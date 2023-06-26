from django.contrib import admin
from .models import Meeting, Contact, Attendee, PendingAttendee, Event, MeetingTime, Conflict, MeetingImmediate

admin.site.register(Meeting)
admin.site.register(Contact)
admin.site.register(Attendee)
admin.site.register(PendingAttendee)
admin.site.register(Event)
admin.site.register(MeetingTime)
admin.site.register(Conflict)
admin.site.register(MeetingImmediate)

class AttendeeInline(admin.StackedInline):
    model = Attendee

class MeetingAdmin(admin.ModelAdmin):
    inlines = [
        AttendeeInline,
    ]

