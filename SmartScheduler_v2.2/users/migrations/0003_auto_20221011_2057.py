# Generated by Django 3.2.16 on 2022-10-12 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_time_end_profile_time_start_profile_timezone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='time_start',
        ),
        migrations.AddField(
            model_name='profile',
            name='time_end_hour',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='time_end_minute',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='time_start_hour',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='time_start_minute',
            field=models.IntegerField(null=True),
        ),
    ]
