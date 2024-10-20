import requests
import json 

# Base URL for the Wikipedia API
BASE_URL = 'https://en.wikipedia.org/w/api.php'

# Create a session object to persist cookies and session
session = requests.Session()

# Fetch a login token
def login_token():        
    params = {
        'action': 'query',
        'meta': 'tokens',
        'type': 'login',
        'format': 'json'
    }

    response = session.get(BASE_URL, params=params)
    if response.status_code == 200:
        login_token = response.json()['query']['tokens']['logintoken']
        return login_token

def login(USERNAME,PASSWORD):
    if USERNAME:
        if PASSWORD:
            # Send a post request to log in using the login token
            login_params = {
                'action': 'clientlogin',
                'format': 'json',
                'loginreturnurl': 'https://en.wikipedia.org/wiki/Main_Page',
                'username': USERNAME,
                'password': PASSWORD,
                'logintoken': login_token()
            }

            login_response = session.post(BASE_URL, data=login_params)
            print(login_response.json())

            # Check for errors
            if 'error' in login_response.json():
                print("Login failed: ", login_response.json()['error']['info'])
            else:
                print("Login successful!")
        else:
            return json.dumps({"error": "not for the password!"})
    else:
        return json.dumps({"error " : "not for the username !"})


# Your Wikipedia username and password
# USERNAME = ''
# PASSWORD = ''

# print(login(USERNAME,PASSWORD))

