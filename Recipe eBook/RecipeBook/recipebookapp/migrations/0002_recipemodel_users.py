# Generated by Django 3.2.16 on 2023-07-09 19:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipebookapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipemodel',
            name='Users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]