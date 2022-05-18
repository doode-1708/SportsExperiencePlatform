from email import message
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv, find_dotenv
import requests

env_path = find_dotenv()
load_dotenv(dotenv_path=env_path)

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
base_api_url = os.getenv('BASE_API_URL')
redirect_uri = os.getenv('REDIRECT_URI')

auth_url = os.getenv('AUTH_URL')
access_url = os.getenv('ACCESS_URL')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": f"Welcome to the Sports Experience Collector API"}

@app.get("/meetup")
def query_meetup(activity, lat, lon, radius):
    results = {}
    grant_type = 'anonymous_code'
    headers = {'Accept': 'application/json'}
    auth_params = {'client_id': client_id, 'response_type': grant_type, 'redirect_uri': redirect_uri}
    auth_response = requests.get(auth_url, params=auth_params, headers=headers)
    auth_token = auth_response.json()["code"]
    access_params = {'client_id': client_id,
                        'client_secret': client_secret,
                        'grant_type': grant_type,
                        'redirect_uri': redirect_uri,
                        'code': auth_token}
    access_response = requests.post(access_url, params=access_params, headers=headers)
    access_token = access_response.json()
    auth_string = 'Bearer %s' % access_token
    oauth_headers = {'Accept': 'application/json', 'Authorization': auth_string}

    query = """query {
        keywordSearch(filter: { query: "%s", lat: %s, lon: %s, radius: %s, source: EVENTS }) {
            count
            pageInfo {
                endCursor
            }
            edges {
                node {
                    id
                }
            }
        }
    }""" % (activity, lat, lon, radius)
    res = requests.post(base_api_url, json={'query': query}, headers=oauth_headers)

    for events in res.json()['data']['keywordSearch']['edges']:
        event_id = events['node']['id']
        query_event = """
            query {
                event(id: %s) {
                    title
                    description
                    dateTime
                    eventUrl
                }
            }
            """ % (event_id)
        res_event = requests.post(base_api_url, json={'query': query_event}, headers=oauth_headers)

        if 'events' not in results.keys():
            results['events'] = []

        results['events'].append(res_event.json()['data']['event'])



    return results
