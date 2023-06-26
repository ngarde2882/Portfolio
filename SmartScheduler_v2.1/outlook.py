from O365 import Account, MSGraphProtocol
import datetime as dt

CLIENT_ID = 'a0b9de60-91e3-4ce4-b53a-105748c12bc7'
#TENANT_URL = 'https://login.microsoftonline.com/68f381e3-46da-47b9-ba57-6f322b8f0da1'
SECRET_ID = '2QH8Q~hicim5TX9g1LPhfu1lrSvjN9wtOhIuAc7u'

credentials = (CLIENT_ID, SECRET_ID)

# define the protocol being used and the scopes of our app
protocol = MSGraphProtocol() 
#protocol = MSGraphProtocol(defualt_resource='<sharedcalendar@domain.com>') 
scopes = 'https://graph.microsoft.com/.default'
account = Account(credentials, protocol=protocol) #, tenant_id = TENANT_URL)

if account.authenticate(scopes=scopes):
   print('Authenticated!')

schedule = account.schedule()
calendar = schedule.get_default_calendar()
q = calendar.new_query('start').greater_equal(dt.datetime(2019, 11, 20))
q.chain('and').on_attribute('end').less_equal(dt.datetime(2023, 11, 24))
#events = calendar.get_events(include_recurring=False) 
events = calendar.get_events(query=q, include_recurring=True) 



for event in events:
    print(event)