from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    start_time = models.TimeField(null=True, default='08:00')
    end_time = models.TimeField(null=True, default='18:00')
    timezone = models.CharField(null=True, max_length=100)
    remember_me = models.BooleanField(null=True, default=False)
    token = models.JSONField(null=True, blank=True)

    # extend the validation
    def clean(self, *args, **kwargs):
        # Don't allow dates older than now.
        if self.end_time <= self.start_time:
            print("Raising validation error...")
            raise ValidationError('End time must be later than start time.')
            

    def __str__(self):
        return f'{self.user.username} Profile'

