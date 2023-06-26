from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import handler403, handler404, handler500
from .views import (
    home,
    pull_in_between,
    push_in_between,
    oauth_endpoint_view,
    rsvp_list,
    rsvp_list_accept,
    rsvp_list_decline,
    rsvp_list_does_not_exist,
    accept_meeting,
    decline_meeting,
    create_attendance_required,
    create_attendance_optional,
    delete_attendance,
    meeting_creation_confirmation,
    add_meeting_contacts,
    meeting_status_schedule,
    custodial_view,
    oauth_landing_view,
    google_calendar_push,
    remember_me_button,

    UserContactListView,
    ContactDetailView,
    ContactCreateView,
    ContactUpdateView,
    ContactDeleteView,

    UserMeetingListView,
    MeetingDetailView,
    MeetingCreateView,
    MeetingUpdateView,
    MeetingDeleteView,
    custom_error_403,
    custom_error_404,

    attendee_in_between,
    attendee_landing,
)
from . import views

urlpatterns = [
    path('', views.blank, name='blank'),
    path('home/', views.home, name='home'),
    path('meetings/<str:username>', UserMeetingListView.as_view(), name='user-meetings'),
    path('meeting/<int:pk>/', MeetingDetailView.as_view(), name='meeting-detail'),
    path('meeting/new/', MeetingCreateView.as_view(), name='meeting-create'),
    path('meeting/<int:pk>/update/', MeetingUpdateView.as_view(), name='meeting-update'),
    path('meeting/<int:pk>/delete', MeetingDeleteView.as_view(), name='meeting-delete'),    

    path('contacts/<str:username>', UserContactListView.as_view(), name='user-contacts'),
    path('contact/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),
    path('contact/new/', ContactCreateView.as_view(), name='contact-create'),
    path('contact/<int:pk>/update/', ContactUpdateView.as_view(), name='contact-update'),
    path('contact/<int:pk>/delete', ContactDeleteView.as_view(), name='contact-delete'),

    path('about/', views.about, name='smart_scheduler-about'),
    path('search_contacts/', views.search_contacts, name='search-contacts'),
    path('rsvp', views.rsvp_list, name='rsvp-list'),
    path('rsvp_accept', views.rsvp_list_accept, name='rsvp-list-accept'),
    path('rsvp_decline', views.rsvp_list_decline, name='rsvp-list-decline'),
    path('rsvp_does_not_exist', views.rsvp_list_does_not_exist, name='rsvp-list-does-not-exist'),
    path('remember_me', views.remember_me_button, name='remember-me'),

    path('accept_meeting/<int:pk>/<int:id>/accept', views.accept_meeting, name='accept-meeting'),
    path('decline_meeting/<int:pk>/<int:id>/decline', views.decline_meeting, name='decline-meeting'),
    path('add_meeting_contacts', views.add_meeting_contacts, name='add-meeting-contacts'),
    path('create_attendance_required/<int:pk>', views.create_attendance_required, name='create-attendance-required'),
    path('create_attendance_optional/<int:pk>', views.create_attendance_optional, name='create-attendance-optional'),
    path('delete_attendance/<int:pk>', views.delete_attendance, name='delete-attendance'),
    path('meeting_status_schedule/<int:pk>', views.meeting_status_schedule, name='meeting-status-schedule'),
    path('custodial_view/<int:pk>', views.custodial_view, name='custodial-view'),
    path('oauth_landing_view/<int:pk>', views.oauth_landing_view, name='oauth-landing-view'),

    path('google_calendar_push/<int:number>/<int:id>', views.google_calendar_push, name='google-calendar-push'),

    path('oauth_endpoint_view/<int:number>', views.oauth_endpoint_view, name='oauth-endpoint-view'),
    path('push_in_between', views.push_in_between, name='push-in-between'),
    path('pull_in_between', views.pull_in_between, name='pull-in-between'),

    path('attendee_in_between', views.attendee_in_between, name='attendee-in-between'),
    path('attendee_landing', views.attendee_landing, name='attendee-landing'),
    path('meeting_creation_confirmation', views.meeting_creation_confirmation, name='meeting-creation-confirmation'),
]
handler403 = custom_error_403
handler404 = custom_error_404

# <app>/<model>_<viewtype>.html
urlpatterns += staticfiles_urlpatterns()

