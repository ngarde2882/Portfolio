# Generated by Django 3.2.16 on 2023-06-29 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, help_text='Author Name', max_length=25)),
                ('Org', models.CharField(blank=True, help_text='Organization Name', max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredientModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(help_text='Ingredient Name', max_length=20)),
                ('Quantity', models.IntegerField(help_text='Ingredient Amount')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(help_text='Recipe Name', max_length=20)),
                ('Directions', models.TextField(help_text='Recipe Directions')),
                ('img', models.ImageField(help_text='Recipe Image', upload_to='images/')),
                ('mealType', models.CharField(help_text='Type of Meal: entree, snack, bread, drink', max_length=20)),
                ('mealtype', models.CharField(blank=True, choices=[('e', 'Entree'), ('b', 'Bread'), ('s', 'Snack'), ('d', 'Drink')], default='n', help_text='Type of Meal: entree, snack, bread, drink', max_length=1)),
                ('Author', models.ManyToManyField(blank=True, help_text='Recipe Author', to='recipebookapp.RecipeAuthor')),
                ('Ingredients', models.ManyToManyField(help_text='Recipe Ingredients', to='recipebookapp.RecipeIngredientModel')),
            ],
            options={
                'ordering': ['Name'],
            },
        ),
    ]