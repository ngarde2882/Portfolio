# Generated by Django 3.2.16 on 2022-11-08 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_profile_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='end_time',
            field=models.TimeField(default='18:00', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='start_time',
            field=models.TimeField(default='08:00', null=True),
        ),
    ]
