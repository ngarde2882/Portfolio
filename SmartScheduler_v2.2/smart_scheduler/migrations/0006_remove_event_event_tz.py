# Generated by Django 3.2.15 on 2022-10-06 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smart_scheduler', '0005_attendee_required_pendingattendee_required'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='event_tz',
        ),
    ]
