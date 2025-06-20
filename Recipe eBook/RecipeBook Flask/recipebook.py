import os
import json
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

def init_db():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            theme_color TEXT DEFAULT '#4285f4'
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            author_id INTEGER,
            name TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            directions TEXT NOT NULL,
            image_path TEXT,
            published BOOLEAN DEFAULT 0,
            likes INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (author_id) REFERENCES users(id)
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            quantity INTEGER,
            units TEXT,
            parishable TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS grocery_lists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            quantity INTEGER,
            units TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            recipe_id INTEGER NOT NULL,
            scheduled_date TEXT NOT NULL, -- format: YYYY-MM-DD
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        );
    """)
    conn.commit()
    conn.close()
init_db()


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.secret_key = "replace-this-with-a-random-secret-key"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form["identifier"]
        password = request.form["password"]

        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password, theme_color FROM users WHERE username = ? OR email = ?", (identifier, identifier))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["theme_color"] = user[3] or "#4285f4"
            return redirect(url_for("dashboard"))

        return "Invalid credentials", 401

    return render_template("login.html")


@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not username or not email or not password:
        return "All fields are required", 400

    try:
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, generate_password_hash(password))
        )
        conn.commit()
        conn.close()
        return redirect(url_for("login"))  # redirect back to login page
    except sqlite3.IntegrityError:
        return "Username or email already taken", 400

@app.route("/recipes")
def recipes():
    user_id = session.get("user_id")
    username = session.get("username")
    theme_color = session.get("theme_color", "#4285f4")

    if not user_id:
        return redirect(url_for("login"))

    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, ingredients, directions, image_path
        FROM recipes
        WHERE user_id = ?
    """, (user_id,))
    
    rows = cursor.fetchall()
    conn.close()

    recipes = [{
        "id": row[0],
        "name": row[1],
        "ingredients": row[2].splitlines(),
        "directions": row[3],
        "image": row[4] or "https://via.placeholder.com/400x200?text=No+Image"
    } for row in rows]

    selected = recipes[0] if recipes else None

    return render_template(
        "recipes.html",
        recipes=recipes,
        recipes_json=json.dumps(recipes),
        selected=selected,
        username=username,
        theme_color=theme_color
    )

# this was for displaying 1 recipe at a time, but now we load all recipes and selectively display on the frontend
# @app.route("/recipes/<int:recipe_id>")
# def view_recipe(recipe_id):
#     user_id = session.get("user_id")
#     username = session.get("username")
#     theme_color = session.get("theme_color", "#4285f4")
#     session["selected"] = recipe_id
#     if not user_id:
#         return redirect(url_for("login"))

#     conn = sqlite3.connect("app.db")
#     cursor = conn.cursor()

#     # Get all recipes for sidebar
#     cursor.execute("SELECT id, name FROM recipes WHERE user_id = ?", (user_id,))
#     recipe_rows = cursor.fetchall()
#     recipes = [{"id": row[0], "name": row[1]} for row in recipe_rows]

#     # Get selected recipe
#     cursor.execute("""
#         SELECT id, name, ingredients, directions, image_path
#         FROM recipes
#         WHERE id = ? AND user_id = ?
#     """, (recipe_id, user_id))
#     row = cursor.fetchone()
#     conn.close()

#     if row is None:
#         return "Recipe not found or unauthorized", 404

#     selected = {
#         "id": row[0],
#         "name": row[1],
#         "ingredients": row[2].splitlines(),
#         "directions": row[3],
#         "image": row[4] or "https://via.placeholder.com/400x200?text=No+Image"
#     }

#     return render_template("dashboard.html", recipes=recipes, selected=selected, username=username, theme_color=theme_color)

@app.route("/recipes/create", methods=["POST"])
def create_recipe():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    name = request.form.get("name", "").strip()
    ingredients = request.form.get("ingredients", "").strip()
    directions = request.form.get("directions", "").strip()
    image = request.files.get("image")

    if not name or not ingredients or not directions:
        return "All fields except image are required.", 400

    # Save image if provided
    image_path = None
    if image and image.filename != "":
        filename = secure_filename(image.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image.save(filepath)
        image_path = filepath

    # Insert recipe
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO recipes (user_id, name, ingredients, directions, image_path)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, name, ingredients, directions, image_path))
    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))

@app.route("/schedule")
def schedule():
    user_id = session.get("user_id")
    username = session.get("username")
    theme_color = session.get("theme_color", "#4285f4")

    if not user_id:
        return redirect(url_for("login"))

    return render_template("schedule.html", username=username, theme_color=theme_color)

if __name__ == "__main__":
    app.run(debug=True)
