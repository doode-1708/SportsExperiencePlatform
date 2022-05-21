from email import message
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from EventCollectorApi.meetup import MeetupQL

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

meetup = MeetupQL()
meetup.get_outh_token()
'''
creates a new meetup api token for querying events
'''

@app.get("/")
def index():
    return {"greeting": f"Welcome to the Sports Experience Collector API"}

@app.get("/meetupql")
def query_meetup(activity, lat, lon, radius):
    result = []
    hasNextPage = False
    meetup = MeetupQL()
    meetup.get_outh_token()
    events = meetup.get_events_by_city(activity, lat, lon, radius)
    hasNextPage = events['data']['keywordSearch']['pageInfo']['hasNextPage']

    for event in events['data']['keywordSearch']['edges']:
        result.append(event['node']['result'])

    while (hasNextPage):
        events = meetup.get_events_by_city(activity, lat, lon, radius, PageCursor=events['data']['keywordSearch']['pageInfo']['endCursor'])
        for event in events['data']['keywordSearch']['edges']:
            result.append(event['node']['result'])
        hasNextPage = events['data']['keywordSearch']['pageInfo']['hasNextPage']

    number_events = len(result)

    event_info = {
        'Info': {
            'EventCount': number_events
        }
        , 'Data': result
    }

    return event_info
