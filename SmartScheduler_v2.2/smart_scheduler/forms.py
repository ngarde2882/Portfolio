from django import forms
from .models import Meeting
from datetime import date, datetime, timedelta
  
def get_closest_friday():
    today = date.today()
    print("Today:")
    print(today)
    # if today is friday, return date one week later
    if date.today().weekday() == 4:
        friday = today + timedelta(days=7)
        return friday
    else:
        friday = today + datetime.timedelta( (4-today.weekday()) % 7 )

# creating a form
class MeetingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        next_friday = get_closest_friday()
        super(MeetingForm, self).__init__(*args, **kwargs)
        self.fields['meeting_description'].required = False
        self.fields['meeting_link_location'].required = False
        f = MeetingForm(initial={'meeting_deadline': next_friday})
    # create meta class
    class Meta:
        # specify model to be used
        model = Meeting
  
        # specify fields to be used
        fields = [
            "meeting_name",
            "meeting_description",
            "meeting_deadline",
            "meeting_duration_hours",
            "meeting_duration_minutes",
            "meeting_link_location",
        ]
    
    