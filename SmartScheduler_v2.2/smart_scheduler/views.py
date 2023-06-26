from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from users.models import Profile
from requests import request
from .forms import MeetingForm
from .models import Meeting, Contact, Attendee, PendingAttendee, Event, MeetingTime, Conflict, MeetingImmediate
from datetime import date, timedelta, time
import json


from .google import *
from .numeric_search import *
from .email_alerts import *

from django.core.exceptions import ObjectDoesNotExist
from django.urls import resolve

def get_closest_friday():
    today = date.today()
    # if today is friday, return date one week later
    if date.today().weekday() == 4:
        friday = today + timedelta(days=7)
        return friday
    else:
        friday = today + datetime.timedelta( (4-today.weekday()) % 7 )

def about(request):
    return render(request, 'smart_scheduler/about.html', {'title': 'About'})

def meeting_status(request):
    context = {
        'meetings' : Meeting.objects.all()
    }
    return render(request, 'smart_scheduler/user_meetings.html', context)

class MeetingAttendance:
    meeting_name = "Default"
    accepted = 0
    pending = 0
    declined = 0

class UserMeetingListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Meeting
    template_name = 'smart_scheduler/user_meetings.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'meetings'
    ordering = ['-date_posted']
    paginate_by = 5
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Meeting.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        meeting_list_info = []
        data = super().get_context_data(**kwargs)
        # Call the base implementation first to get a context
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        meetings = Meeting.objects.filter(author=user)
        for meeting in meetings:
            meeting_attendance = MeetingAttendance()
            meeting_attendance.id = meeting.id
            accepted_count = Attendee.objects.filter(rsvp_status='Accepted').filter(meeting_name_id = meeting.id).count()
            pending_count = Attendee.objects.filter(rsvp_status='Pending').filter(meeting_name_id = meeting.id).count()
            declined_count = Attendee.objects.filter(rsvp_status='Declined').filter(meeting_name_id = meeting.id).count()
            # delete meeting if nobody was invited
            if (accepted_count + pending_count + declined_count) <= 0:
                print("Deleting the empty meeting.")
                meeting.delete()


        for meeting in meetings:
            meeting_attendance = MeetingAttendance()
            meeting_attendance.id = meeting.id
            meeting_attendance.accepted = Attendee.objects.filter(rsvp_status='Accepted').filter(meeting_name_id = meeting.id).count()
            meeting_attendance.pending = Attendee.objects.filter(rsvp_status='Pending').filter(meeting_name_id = meeting.id).count()
            meeting_attendance.declined = Attendee.objects.filter(rsvp_status='Declined').filter(meeting_name_id = meeting.id).count()
            meeting_list_info.append(meeting_attendance)
        data['meeting_list_info'] = meeting_list_info
        return data
    
    # verifies that logged in user is the author of a post and can therefore edit
    def test_func(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        if self.request.user == user:
            return True
        return False

# list view the detailed attendee_status
class MeetingDetailView(DetailView):
    model = Meeting


# create a attendee_status with parameters
class MeetingCreateView(LoginRequiredMixin, CreateView):
    
    model = Meeting
    fields = ['meeting_name', 'meeting_description', 'meeting_start', 'meeting_deadline', 'meeting_duration_hours', 'meeting_duration_minutes', 'meeting_link_location']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('custodial-view', args={self.object.id})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        day_start = Profile.objects.filter(user=self.request.user).first().start_time
        day_end = Profile.objects.filter(user=self.request.user).first().end_time
        #day_length = day_end - day_start
        pending_attendees = PendingAttendee.objects.filter(meeting_creator_name=self.request.user)
        #data['day_length'] = day_length
        data['pending_attendees'] = pending_attendees
        return data

@login_required
def remember_me_button(request):
    user = Profile.objects.filter(user = request.user).first()
    if user.remember_me == True:
        Profile.objects.filter(user=request.user).update(remember_me=False)
        print("Remember me is currently True. Setting to False.")
    else:
        Profile.objects.filter(user=request.user).update(remember_me=True)
        print("Remember me is currently False. Setting to True.")
    return redirect('meeting-create')

@login_required
def home(request):
    return HttpResponseRedirect(
               reverse('user-meetings', 
                       args=[request.user.username]))

def blank(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return HttpResponseRedirect(reverse('user-meetings', args=[request.user.username]))

# custodial view pulls the events from the meeting creator's calendar and uploads to database
# adds pending attendees to attendees table
# deletes pending attendees
# sends email invitations to attendees
@login_required
def custodial_view(request, pk):
    request.session['meeting_primary_key'] = pk
    author = request.user
    meeting_info = Meeting.objects.filter(id = pk).first()
    token = Profile.objects.filter(user=author).first().token
    print("The token is ", str(token))
    print("The primary key in the custodial view is: ", str(pk))
    if not token:
        print('token not found')
        SCOPES = ['https://www.googleapis.com/auth/calendar.events']
        redirect_uri = 'https://django-smart-scheduler.herokuapp.com/pull_in_between'
        state = request.GET.get('state',None)
        google = google_auth_oauthlib.flow.Flow.from_client_secrets_file('credentials.json',scopes=SCOPES,state=state)
        google.redirect_uri = redirect_uri
        authorization_url = generate_oauth(google)
        print("Redirecting to authorization_url: ", str(authorization_url))
        return HttpResponseRedirect(authorization_url)
    else:
        print('token_found')
        pk = request.session.get('meeting_primary_key', None)
        return HttpResponseRedirect(
                reverse('oauth-landing-view', 
                        args=[pk]))

def oauth_landing_view(request, pk):
    email_list = []
    attendee_pk_list = []
    meeting_name_id_list = []
    meeting_info = Meeting.objects.filter(id = pk).first()
    deadline = meeting_info.meeting_deadline
    event_owner = Meeting.objects.filter(id = pk).first().author 
    
    token = Profile.objects.filter(user=request.user).first().token
    if not token:
        SCOPES = ['https://www.googleapis.com/auth/calendar.events']
        client_id = "47823843627-39ukleg5hs35p2cnplpa4d1fqem953kg.apps.googleusercontent.com"
        redirect_uri = 'https://django-smart-scheduler.herokuapp.com/pull_in_between'
        state = request.GET.get('state',None)
        google = google_auth_oauthlib.flow.Flow.from_client_secrets_file('credentials.json',scopes=SCOPES,state=state)
        google.redirect_uri = redirect_uri
        url = request.session.get('url', None)
        generate_token(google, request.user, url)

    # # if the token fails (due to an old token), reroute the user back through custodial view for token generation
    # if not GCal_Pull(deadline, request, pk, author, event_owner, meeting_info, True):
    #     return HttpResponseRedirect(
    #             reverse('custodial-view',
    #                     args=[pk]))
    GCal_Pull(deadline, request, pk, request.user, event_owner, meeting_info, True)
    # pull the event timezone and store it under the current user's timezone
    try:
        time = Event.objects.filter(event_owner = event_owner).first().event_start
        time = time[-6:]
    except:
        time = '-06:00' # if the user has no events on their calendar we cannot find their timezone, currently setting default timezone to -06:00 for winter CST
    Profile.objects.filter(user=request.user).update(timezone=time)
    print("Time: ", str(time))
    # get the info from the pending attendees
    pending_attendees = PendingAttendee.objects.filter(meeting_creator_name=request.user)
    meeting = Meeting.objects.filter(id=pk)
    for pending_attendee in pending_attendees:
        # write and save to the official attendees table
        if pending_attendee.required == True:
            attendee = Attendee(attendee_name=pending_attendee.attendee_name, email_address=pending_attendee.email_address, rsvp_status='Pending', meeting_name_id=pk, required=True)
            attendee.save()
        else:
            attendee = Attendee(attendee_name=pending_attendee.attendee_name, email_address=pending_attendee.email_address, rsvp_status='Pending', meeting_name_id=pk, required=False)
            attendee.save()

    # delete the pending attendees
    PendingAttendee.objects.filter(meeting_creator_name=request.user).delete()
    Attendees = Attendee.objects.filter(meeting_name_id=pk)
    for attendee in Attendees:
        meeting_name_id_list.append(attendee.meeting_name_id)
        email_list.append(attendee.email_address)
        print("Appending ", str(attendee.email_address), " to the list.")
        attendee_pk_list.append(attendee.id)
        #print("Attendee: " + str(attendee.attendee_name))
        #print("Attendee id: " + str(attendee.id))
        #print("Meeting name id: " + str(attendee.meeting_name_id))

    meeting_name_object = MeetingImmediate(meeting_name=meeting_info, meeting_id=pk)
    meeting_name_object.save()

    # send the invitation email
    meeting_name = meeting_info.meeting_name
    meeting_description = meeting_info.meeting_description
    meeting_deadline = meeting_info.meeting_deadline
    duration_hours = meeting_info.meeting_duration_hours
    duration_minutes = meeting_info.meeting_duration_minutes
    meeting_link_location = meeting_info.meeting_link_location

    send_invitation(
        meeting_name_id_list,
        email_list,
        attendee_pk_list,
        meeting_name,
        meeting_description,
        meeting_deadline,
        duration_hours,
        duration_minutes,
        meeting_link_location
    )
    return HttpResponseRedirect(
               reverse('user-meetings', 
                       args=[request.user.username]))

class MeetingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Meeting
    fields = ['meeting_name', 'meeting_description', 'meeting_deadline', 'meeting_duration_hours', 'meeting_duration_minutes', 'meeting_link_location']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # verifies that logged in user is the author of a post and can therefore edit
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
    def get_success_url(self):
        return reverse_lazy('user-meetings', args={self.object.author})

# list view the detailed post
class MeetingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Meeting
    success_url = '/'
    # verifies that logged in user is the author of a post and can therefore edit
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False   
    
    def get_success_url(self):
        return reverse_lazy('user-meetings', args={self.object.author})

def contacts(request):
    context = {
        'contacts' : Contact.objects.all()
    }
    return render(request, 'smart_scheduler/user_contacts.html', context)

class UserContactListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Contact
    template_name = 'smart_scheduler/user_contacts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'contacts'
    ordering = ['-date_posted']
    paginate_by = 5
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Contact.objects.filter(author=user).order_by('contact_name').values()
    
    # verifies that logged in user is the author of a post and can therefore edit
    def test_func(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        if self.request.user == user:
            return True
        return False

# list view the detailed attendee_status
class ContactDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Contact
    # verifies that logged in user is the author of a post and can therefore edit
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# create a attendee_status with parameters
class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    fields = ['contact_name', 'email_address']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('user-contacts', args={self.object.author})


class ContactUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Contact
    fields = ['contact_name', 'email_address']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # verifies that logged in user is the author of a post and can therefore edit
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('user-contacts', args={self.object.author})

# list view the detailed post
class ContactDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Contact
    success_url = '/'
    # verifies that logged in user is the author of a post and can therefore edit
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False  

    def get_success_url(self):
        return reverse_lazy('user-contacts', args={self.object.author}) 


def custom_error_403(request, exception):
    return render(request, '403.html', {})

def custom_error_404(request, exception):
    context = {}
    return render(request, '404.html', context)

@login_required
def search_contacts(request):
    if request.method == "POST":
        searched = request.POST['searched']
        contacts = Contact.objects.filter(author=request.user, contact_name__icontains=searched).order_by('contact_name') | Contact.objects.filter(author=request.user, email_address__icontains=searched).order_by('contact_name')
        contacts_count = Contact.objects.filter(author=request.user, contact_name__icontains=searched).order_by('contact_name').count() + Contact.objects.filter(author=request.user, email_address__icontains=searched).order_by('contact_name').count()
        return render(request, 
        'smart_scheduler/user_contacts.html', 
        {'searched': searched,
         'contacts': contacts,
         'contacts_count': contacts_count,
        })
    else:
        return render(request, 
        'smart_scheduler/user_contacts.html', 
        {})

@login_required
def rsvp_list(request):
    if request.method == "POST":
        searched = request.POST['searched']
        invites = Attendee.objects.filter(attendee_name__icontains=searched).filter(rsvp_status="Pending").order_by('attendee_name') | Attendee.objects.filter(email_address__icontains=searched).filter(rsvp_status="Pending").order_by('attendee_name')
        invite_count = Attendee.objects.filter(attendee_name__icontains=searched).filter(rsvp_status="Pending").order_by('attendee_name').count() + Attendee.objects.filter(email_address__icontains=searched).filter(rsvp_status="Pending").order_by('attendee_name').count()
        return render(request, 
        'smart_scheduler/rsvp.html', 
        {'searched': searched,
         'invites': invites,
         'invite_count': invite_count,
        })
    else:
        return render(request, 
        'smart_scheduler/rsvp.html', 
        {})

"""
def accept_meeting_outlook(request, pk, id):
    meeting = Meeting.objects.filter(id=pk).first()
    meeting_name = Meeting.objects.filter(id=pk).first().meeting_name
    meeting_name_object = MeetingImmediate(meeting_name=meeting_name, meeting_id=pk)
    meeting_name_object.save()
    context = initialize_context(request)
    attendee_status = Attendee.objects.get(pk=id)
    attendee_status.rsvp_status = 'Accepted'
    attendee_status.save()
    return redirect('signin')
"""
def rsvp_list_accept(request):
    return render(request, 
    'smart_scheduler/accept.html', 
    {})

def meeting_creation_confirmation(request):
    return render(request, 
    'smart_scheduler/meeting_creation_confirmation.html', 
    {})

def rsvp_list_decline(request):
    return render(request, 
    'smart_scheduler/decline.html', 
    {})

def rsvp_list_does_not_exist(request):
    return render(request, 
    'smart_scheduler/does_not_exist.html', 
    {})

def accept_meeting(request, pk, id):
    attendee = Attendee.objects.filter(pk=id).first()
    request.session['pk'] = pk
    try:
        meeting_author = Meeting.objects.filter(id=pk).first().author
    except:
        print("Exception occurred.")
        return redirect('rsvp-list-does-not-exist')
    
    new_id = Contact.objects.filter(contact_name=attendee.attendee_name, author=meeting_author).first().id
    # print('newid:',new_id)
    # print('Contact:',Contact.objects.filter(id=new_id).first())
    request.session['id'] = new_id
    print('id in')
    
    try:
        attendee_status = Attendee.objects.get(pk=id)
        print("Attendee found!")
        event_owner = Attendee.objects.filter(id = id).first().attendee_name
        meeting_info = Meeting.objects.filter(id = pk).first()
        deadline = meeting_info.meeting_deadline
        author = meeting_author
        
        #GCal_Pull(deadline, request, pk, author, event_owner, meeting_info)

        attendee_status = Attendee.objects.get(pk=id)
        attendee_status.rsvp_status = 'Accepted'
        attendee_status.save()
        # deleting any existing events in the database for this person under this meeting
        attendee_name = Attendee.objects.get(pk=id).attendee_name
        events = Event.objects.filter(event_owner=str(attendee_name), meeting=pk).delete()
        print("Attendee status saved.")

        return redirect('attendee-in-between')
    except:
        print("Exception occurred.")
        return redirect('rsvp-list-does-not-exist')

def attendee_in_between(request):
    id = request.session.get('id',None)
    token = Contact.objects.filter(pk=id).first().token
    if not token:
        SCOPES = ['https://www.googleapis.com/auth/calendar.events']
        client_id = "47823843627-39ukleg5hs35p2cnplpa4d1fqem953kg.apps.googleusercontent.com"
        redirect_uri = 'https://django-smart-scheduler.herokuapp.com/attendee_landing'
        # google = OAuth2Session(client_id, scope=SCOPES, redirect_uri=redirect_uri)
        state = request.GET.get('state',None)
        google = google_auth_oauthlib.flow.Flow.from_client_secrets_file('credentials.json',scopes=SCOPES,state=state)
        google.redirect_uri = redirect_uri
        authorization_url = generate_oauth(google)
        print("Redirecting to authorization_url: ", str(authorization_url))
        return HttpResponseRedirect(authorization_url)
    else:
        return HttpResponseRedirect(
            reverse('attendee-landing'))

def attendee_landing(request):
    id = request.session.get('id',None)
    pk = request.session.get('pk',None)
    event_owner = Contact.objects.filter(id = id).first().contact_name
    meeting_info = Meeting.objects.filter(id = pk).first()
    deadline = meeting_info.meeting_deadline
    token = Contact.objects.filter(pk=id).first().token
    if not token:
        SCOPES = ['https://www.googleapis.com/auth/calendar.events']
        client_id = "47823843627-39ukleg5hs35p2cnplpa4d1fqem953kg.apps.googleusercontent.com"
        redirect_uri = 'https://django-smart-scheduler.herokuapp.com/attendee_landing'
        # google = OAuth2Session(client_id, scope=SCOPES, redirect_uri=redirect_uri)
        state = request.GET.get('state',None)
        google = google_auth_oauthlib.flow.Flow.from_client_secrets_file('credentials.json',scopes=SCOPES,state=state)
        google.redirect_uri = redirect_uri
        url = request.build_absolute_uri()
        generate_contact_token(google, request.user, url, id)
    
    # if not GCal_Pull(deadline, request, pk, request.user, event_owner, meeting_info, False):
    #     return HttpResponseRedirect(reverse('attendee-in-between'))
    GCal_Pull(deadline, request, pk, request.user, event_owner, meeting_info, False)
    return redirect('rsvp-list-accept')

def decline_meeting(request, pk, id):
    try:
        attendee_status = Attendee.objects.get(pk=id)
        attendee_name = Attendee.objects.get(pk=id).attendee_name
        print("The attendee name is ", str(attendee_name))
    except:
        print("Exception occurred for decline.")
        return redirect('rsvp-list-does-not-exist')
    try:
        # checking if the events exist
        events = Event.objects.filter(event_owner=str(attendee_name), meeting=pk).delete()
        print("The attendee has events. Need to delete them.")

    except:
        print("The attendee has no events.")
    attendee_status.rsvp_status = 'Declined'
    attendee_status.save()
    return redirect('rsvp-list-decline')

@login_required
def add_meeting_contacts(request):
    pending_attendees = PendingAttendee.objects.filter(meeting_creator_name=request.user)
    contacts = Contact.objects.filter(author=request.user).order_by('contact_name') 

    for pending_attendee in pending_attendees:
        for contact in contacts:
            if (pending_attendee.attendee_name == contact.contact_name):
                contacts = contacts.exclude(contact_name=pending_attendee.attendee_name)
    if request.method == "POST":
        searched = request.POST['searched']
        contacts = Contact.objects.filter(author=request.user, contact_name__icontains=searched).order_by('contact_name') | Contact.objects.filter(author=request.user, email_address__icontains=searched).order_by('contact_name')
        for pending_attendee in pending_attendees:
            for contact in contacts:
                if (pending_attendee.attendee_name == contact.contact_name):
                    print(str(pending_attendee.attendee_name), " and ", str(contact.contact_name), "are the same.")
                    contacts = contacts.exclude(contact_name=pending_attendee.attendee_name)
        contacts_count = Contact.objects.filter(author=request.user, contact_name__icontains=searched).order_by('contact_name').count() + Contact.objects.filter(author=request.user, email_address__icontains=searched).order_by('contact_name').count()
        return render(request, 
        'smart_scheduler/add_attendees.html',
        {'current_attendees': pending_attendees,
         'searched': searched,
         'contacts': contacts,
         'contacts_count': contacts_count,
         'all_contacts': contacts,
        })
    else:
        return render(request, 
        'smart_scheduler/add_attendees.html', 
        {'current_attendees': pending_attendees,
         'all_contacts': contacts,
        })

@login_required
def create_attendance_required(request, pk):
    contact = Contact.objects.get(pk=pk)
    # toggle attendee pending status to true
    pending_attendee = PendingAttendee(attendee_name=contact.contact_name, email_address=contact.email_address, meeting_creator_name=request.user, required=True)
    # prevents other users from seeing data
    if not request.user == pending_attendee.meeting_creator_name:
        return redirect('smart_scheduler-about')
    contact = Contact.objects.get(pk=pk)
    if not PendingAttendee.objects.filter(attendee_name=contact.contact_name).filter(meeting_creator_name=request.user).exists():
        pending_attendee.save()
    return redirect('add-meeting-contacts')

@login_required
def create_attendance_optional(request, pk):
    contact = Contact.objects.get(pk=pk)
    # toggle attendee pending status to true
    pending_attendee = PendingAttendee(attendee_name=contact.contact_name, email_address=contact.email_address, meeting_creator_name=request.user, required=False)
    # prevents other users from seeing data
    if not request.user == pending_attendee.meeting_creator_name:
        return redirect('smart_scheduler-about')
    contact = Contact.objects.get(pk=pk)
    if not PendingAttendee.objects.filter(attendee_name=contact.contact_name).filter(meeting_creator_name=request.user).exists():
        pending_attendee.save()
    return redirect('add-meeting-contacts')

@login_required
def delete_attendance(request, pk):
    pending_attendee = PendingAttendee.objects.get(pk=pk)
    pending_attendee.delete()
    return redirect('add-meeting-contacts')
        
@login_required
def meeting_status_schedule(request, pk):
    meeting = Meeting.objects.get(pk=pk)
    meeting_id = pk
    MeetingTime.objects.filter(meeting=meeting.id).delete()
    # prevents other users from seeing data
    if not request.user == meeting.author:
        return redirect('smart_scheduler-about') 
    attendee_accepted = Attendee.objects.filter(meeting_name=meeting.id).filter(rsvp_status='Accepted')
    attendee_pending = Attendee.objects.filter(meeting_name=meeting.id).filter(rsvp_status='Pending')
    attendee_declined = Attendee.objects.filter(meeting_name=meeting.id).filter(rsvp_status='Declined')
    today_date = date.today()
    deadline_date = meeting.meeting_deadline
    days_remaining = deadline_date - today_date
    deadline_string = deadline_date.strftime("%b %d, %Y") + " 18:00:00"
    print(deadline_string)

    if request.method == "POST":
        searched = request.POST['searched']
        deadline = Meeting.objects.filter(id=pk).first().meeting_deadline
        duration_hours = Meeting.objects.filter(id=pk).first().meeting_duration_hours
        duration_minutes = Meeting.objects.filter(id=pk).first().meeting_duration_minutes
        last_day = MeetingFormat(deadline.month, deadline.day, deadline.year, duration_hours, duration_minutes, pk)
        best = numeric_search(last_day, int(searched), pk)
        conflicts = Conflict.objects.filter(meeting=pk)
        print(best)
        best_times(best, pk)
        meeting_times = MeetingTime.objects.filter(meeting=pk)
        meeting_times_adjusted = meeting_times
        for meeting_time_adjusted in meeting_times_adjusted:
            if int(meeting_time_adjusted.time_hours) > 12:
                integer_holder = int(meeting_time_adjusted.time_hours) - 12
                meeting_time_adjusted.time_hours = str(integer_holder)
        return render(request, 
        'smart_scheduler/meeting_status_schedule.html', 
        {
            'conflicts': conflicts,
            'meeting_id': meeting_id,
            'deadline_string': deadline_string,
            'searched': searched,
            'meeting_times_adjusted': meeting_times_adjusted,
            'meeting_times': meeting_times,
            'meeting': meeting,
            'attendee_accepted': attendee_accepted,
            'attendee_pending': attendee_pending,
            'attendee_declined': attendee_declined,
            'days_remaining': days_remaining,
        })
    else:
        return render(request, 
        'smart_scheduler/meeting_status_schedule.html', 
        {
            'meeting_id': meeting_id,
            'deadline_string': deadline_string,
            'meeting': meeting,
            'attendee_accepted': attendee_accepted,
            'attendee_pending': attendee_pending,
            'attendee_declined': attendee_declined,
            'days_remaining': days_remaining,
        })

def pull_in_between(request):
    pk = request.session.get('meeting_primary_key', None)
    url = request.build_absolute_uri()
    request.session['url'] = url
    return HttpResponseRedirect(
               reverse('oauth-landing-view', 
                       args=[pk]))

def push_in_between(request):
    pk = request.session.get('meeting_primary_key', None)
    url = request.build_absolute_uri()
    request.session['url'] = url
    return HttpResponseRedirect(
               reverse('oauth-endpoint-view', 
                       args=[pk]))

def oauth_endpoint_view(request, number):
    print("The meeting primary key you are looking for is: ", number)
    meeting = Meeting.objects.filter(id=number).first()
    meeting_length_hours = meeting.meeting_duration_hours
    meeting_length_minutes = meeting.meeting_duration_minutes
    meeting_time_id = request.session.get('meeting_time_primary_key', None)
    print("The meeting time id is: ", meeting_time_id)
    date = MeetingTime.objects.filter(id=meeting_time_id).first().date
    start = MeetingTime.objects.filter(id=meeting_time_id).first().start
    length = meeting_length_hours * 4 + meeting_length_minutes / 15
    description = meeting.meeting_description
    summary = meeting.meeting_name
    location = meeting.meeting_link_location
    attendees = Attendee.objects.filter(meeting_name=number).filter(rsvp_status='Accepted')
    print("THE ATTENDEES ARE: ", attendees)
    attendee_emails = []
    for x in attendees:
        attendee_emails.append(x.email_address)
    meeting_creator_email = []
    meeting_creator_email.append(request.user.email)
    token = Profile.objects.filter(user=request.user).first().token
    if not token:
        SCOPES = ['https://www.googleapis.com/auth/calendar.events']
        client_id = "47823843627-39ukleg5hs35p2cnplpa4d1fqem953kg.apps.googleusercontent.com"
        redirect_uri = 'https://django-smart-scheduler.herokuapp.com/push_in_between'
        # google = OAuth2Session(client_id, scope=SCOPES, redirect_uri=redirect_uri)
        state = request.GET.get('state',None)
        google = google_auth_oauthlib.flow.Flow.from_client_secrets_file('credentials.json',scopes=SCOPES,state=state)
        google.redirect_uri = redirect_uri
        url = request.session.get('url', None)
        generate_token(google, request.user, url)
    # if not GCal_push(date, start, length, summary, description, location, attendee_emails, user_email):
    #     return HttpResponseRedirect(reverse('google-calendar-push'))
    GCal_push(date, start, length, summary, description, location, attendee_emails, meeting_creator_email)
    # sending confirmation email
    meeting_confirmation(
        date,
        meeting_creator_email,
        summary,
        description,
        start,
        meeting_length_hours,
        meeting_length_minutes,
        location
    )
    # delete the meeting
    meeting = Meeting.objects.filter(id=number).first()
    meeting.delete()
    return redirect('meeting-creation-confirmation')

def google_calendar_push(request, number, id):
    print("The meeting primary key in the google_calendar_push view is: ", number)
    meeting = Meeting.objects.filter(id=number).first()
    request.session['meeting_time_primary_key'] = id
    meeting_length_hours = meeting.meeting_duration_hours
    meeting_length_minutes = meeting.meeting_duration_minutes
    date = MeetingTime.objects.filter(id=id).first().date
    start = MeetingTime.objects.filter(id=id).first().start
    length = meeting_length_hours * 4 + meeting_length_minutes / 15
    description = meeting.meeting_description
    summary = meeting.meeting_name
    location = meeting.meeting_link_location
    attendees = Attendee.objects.filter(meeting_name=number).filter(rsvp_status='Accepted')
    attendee_emails = []
    for attendee in attendees:
        attendee_emails.append(str(attendee.email_address))
    token = Profile.objects.filter(user=request.user).first().token
    if not token:
        print('token not found')
        SCOPES = ['https://www.googleapis.com/auth/calendar.events']
        redirect_uri = 'https://django-smart-scheduler.herokuapp.com/push_in_between'
        state = request.GET.get('state',None)
        google = google_auth_oauthlib.flow.Flow.from_client_secrets_file('credentials.json',scopes=SCOPES,state=state)
        google.redirect_uri = redirect_uri
        authorization_url = generate_oauth(google)
        return HttpResponseRedirect(authorization_url)
    else:
        return HttpResponseRedirect(
               reverse('oauth-endpoint-view', 
                       args=[number]))