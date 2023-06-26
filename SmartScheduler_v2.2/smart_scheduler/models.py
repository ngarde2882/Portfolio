from email.policy import default
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from datetime import date, timedelta, datetime

class Meeting(models.Model):
    meeting_name = models.CharField(max_length=100)
    meeting_description = models.TextField(blank=True)
    meeting_start = models.DateField(default=date.today)
    meeting_deadline = models.DateField(default=date.today)
    meeting_duration_hours = models.IntegerField()
    meeting_duration_minutes = models.IntegerField()
    meeting_link_location = models.CharField(max_length=100, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # extend the validation
    def clean(self, *args, **kwargs):
        # run the base validation
        super(Meeting, self).clean(*args, **kwargs)

        # Don't allow dates older than now.
        if self.meeting_deadline < date.today():
            raise ValidationError('Enter a deadline today or later.')

    def __str__(self):
        return self.meeting_name
    
    def get_absolute_url(self):
        return reverse("meeting-detail", kwargs={"pk": self.pk})


class MeetingImmediate(models.Model):
    meeting_name = models.CharField(max_length=100)
    meeting_id = models.IntegerField(default=1)

    def __str__(self):
        return self.meeting_name
    
    def get_absolute_url(self):
        return reverse("meeting-detail", kwargs={"pk": self.pk})

class Contact(models.Model):
    contact_name = models.CharField(max_length=100)
    email_address = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    remember_me = models.BooleanField(default=False)
    token = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.contact_name
    
    def get_absolute_url(self):
        return reverse("contact-detail", kwargs={"pk": self.pk})

# ensure a user cannot have multiple meetings of the same name
class Attendee(models.Model):
    attendee_name = models.CharField(max_length=100)
    required = models.BooleanField(default=True)
    email_address = models.CharField(max_length=100)
    rsvp_status = models.CharField(max_length=100)
    meeting_name = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.attendee_name
    
    def get_absolute_url(self):
        return reverse("contact-detail", kwargs={"pk": self.pk})

class PendingAttendee(models.Model):
    attendee_name = models.CharField(max_length=100)
    required = models.BooleanField(default=True)
    email_address = models.CharField(max_length=100)
    meeting_creator_name = models.CharField(max_length=100)

    def __str__(self):
        return self.attendee_name
    
    def get_absolute_url(self):
        return reverse("contact-detail", kwargs={"pk": self.pk})


class Event(models.Model):
    event_owner = models.CharField(max_length=100)
    event_start = models.CharField(max_length=100)
    event_end = models.CharField(max_length=100)
    event_number_of_people = models.IntegerField()
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)

    def __str__(self):
        return self.event_owner
    
    def get_absolute_url(self):
        return reverse("contact-detail", kwargs={"pk": self.pk})

class MeetingTime(models.Model):
    day = models.CharField(max_length=100)
    month = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    weekday = models.CharField(max_length=100)
    time_hours = models.CharField(max_length=100)
    time_minutes = models.CharField(max_length=100)
    am_or_pm = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    start = models.IntegerField(default=800)

    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)

    def __str__(self):
        return self.day
    
    def get_absolute_url(self):
        return reverse("contact-detail", kwargs={"pk": self.pk})

class Conflict(models.Model):
    name = models.CharField(max_length=100)
    meeting_time = models.ForeignKey(MeetingTime, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("contact-detail", kwargs={"pk": self.pk})