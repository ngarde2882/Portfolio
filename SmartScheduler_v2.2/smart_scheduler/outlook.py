"""
import yaml
import msal
import os
import time

# Load the oauth_settings.yml file located in your app DIR
stream = open('oauth_settings.yml', 'r')
settings = yaml.load(stream, yaml.SafeLoader)

def load_cache(request):
  # Check for a token cache in the session
  cache = msal.SerializableTokenCache()
  if request.session.get('token_cache'):
    cache.deserialize(request.session['token_cache'])
  return cache

def save_cache(request, cache):
  # If cache has changed, persist back to session
  if cache.has_state_changed:
    request.session['token_cache'] = cache.serialize()

def get_msal_app(cache=None):
  # Initialize the MSAL confidential client
  auth_app = msal.ConfidentialClientApplication(
    settings['app_id'],
    authority=settings['authority'],
    client_credential=settings['app_secret'],
    token_cache=cache)
  return auth_app

# Method to generate a sign-in flow
def get_sign_in_flow():
  auth_app = get_msal_app()
  return auth_app.initiate_auth_code_flow(
    settings['scopes'],
    redirect_uri=settings['redirect'])

# Method to exchange auth code for access token
def get_token_from_code(request):
  cache = load_cache(request)
  auth_app = get_msal_app(cache)

  # Get the flow saved in session
  flow = request.session.pop('auth_flow', {})
  result = auth_app.acquire_token_by_auth_code_flow(flow, request.GET)
  save_cache(request, cache)

  return result


def store_user(request, user):
  try:
    request.session['user'] = {
      'is_authenticated': True,
      'name': user['displayName'],
      'email': user['mail'] if (user['mail'] != None) else user['userPrincipalName'],
      'timeZone': user['mailboxSettings']['timeZone'] if (user['mailboxSettings']['timeZone'] != None) else 'UTC'
    }
  except Exception as e:
    print(e)

def get_token(request):
  cache = load_cache(request)
  auth_app = get_msal_app(cache)

  accounts = auth_app.get_accounts()
  if accounts:
    result = auth_app.acquire_token_silent(
      settings['scopes'],
      account=accounts[0])
    save_cache(request, cache)

    return result['access_token']

def remove_user_and_token(request):
  if 'token_cache' in request.session:
    del request.session['token_cache']

  if 'user' in request.session:
    del request.session['user']




"""
"""
from os import access
import requests
from ms_graph import generate_access_token, GRAPH_API_ENDPOINT

APP_ID = '3e9e8131-2909-47df-8439-f793a1556cde'
SCOPES = ['Calendars.ReadWrite']

# Step 1: Generate access token
access_token = generate_access_token(APP_ID, SCOPES)
headers = {
    'Authorization': 'Bearer ' + access_token['access_token']
}

# Step 2: Create an event
def construct_event_detail(event_name, **event_details):
    request_body = {
        'subject': event_name
    }
    for key, val in event_details.items():
        request_body[key] = val
    return request_body

response1_create = requests.post(
    GRAPH_API_ENDPOINT + f'/me/events',
    headers=headers,
    json=construct_event_detail('Movie Night')
)
print(response1_create.json())

"""

"""
import webbrowser
import requests
import msal
from msal import ConfidentialClientApplication

APPLICATION_ID = '3e9e8131-2909-47df-8439-f793a1556cde'
CLIENT_SECRET = 'QXw8Q~9Y6qvIdk~MIhXUcHZB2YZoXVzj83xUUbFO'
authority_url = 'https://login.microsoftonline.com/consumers/'
base_url = 'https://graph.microsoft.com/v1.0/'
SCOPES = ['User.Read']

# method 1: authentication with authorization code
client_instance = ConfidentialClientApplication(
    client_id = APPLICATION_ID,
    client_credential = CLIENT_SECRET
)
authorization_request_url = client_instance.get_authorization_request_url(SCOPES)
print(authorization_request_url)
webbrowser.open(authorization_request_url)


authorization_code = 'M.R3_SN1.d0b83b8c-9654-ae5c-fe0c-dac3858306ec'
access_token = client_instance.acquire_token_by_authorization_code(
    code=authorization_code,
    scopes=SCOPES
)
print("")
print("")
print("Help")
print(access_token)
print("Help")
print("")
print("")

access_token_id = access_token['access_token']
headers = {'Authorization': 'Bearer ' + access_token_id}
endpoint = base_url + 'me'
response = requests.get(endpoint, headers=headers)
print(response)
print(response.json())


"""