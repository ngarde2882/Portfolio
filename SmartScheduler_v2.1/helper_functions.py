def full_name_function(first_name, last_name):
    full_name = first_name + " " + last_name
    return full_name

# function that allows a meeting organizer to view the realtime status of meeting invitations
def view_pending_members():
  # adding a title to the function
  st.title("Pending Member Status")
  # reference to all of the meetings under the logged-in user
  all_meetings = db.child("User").child(user['localId']).child("Meetings").get()
  # if there are meetings existing under the user
  if all_meetings.each() is not None:
    # iterate through all of the meetings
    for i in all_meetings.each():
      # creating empty arrays that will hold all members that are attending and that are not attending separately
      attending_list = []
      not_attending_list = []
      # list the 
      st.header(i.key())
      all_attending = db.child("User").child(user['localId']).child("Meetings").child(i.key()).child("Attendee List").child("Attending").get()
      if all_attending.each() is not None:
        for j in all_attending.each():
          attending_list.append(j.val())
        all_not_attending = db.child("User").child(user['localId']).child("Meetings").child(i.key()).child("Attendee List").child("Not Attending").get()
        if all_not_attending.each() is not None:
          for k in all_not_attending.each():
            not_attending_list.append(k.val())
      col1, col2 = st.columns(2) 
      with col1:
        st.header("Attending")
        for i in attending_list:
          st.write(i)
      with col2:
        st.header("Not Attending")
        for i in not_attending_list:
          st.write(i)
      if st.button('OVERRIDE AND SCHEDULE MEETING'):
        st.success("Meeting Scheduled!")