from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        # TODO: Add authentication logic
        return redirect(url_for("dashboard"))  # Placeholder redirect
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return "<h2>Welcome to your dashboard!</h2>"

if __name__ == "__main__":
    app.run(debug=True)
