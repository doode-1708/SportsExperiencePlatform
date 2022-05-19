import os
from dotenv import load_dotenv, find_dotenv
import requests

class MeetupQL():
    def __init__(self):
        '''
        read all needed configuration parameters for oauth process from .env
        '''
        env_path = find_dotenv()
        load_dotenv(dotenv_path=env_path)

        #self.client_id = os.getenv('CLIENT_ID')
        #self.client_secret = os.getenv('CLIENT_SECRET')
        #self.base_api_url = os.getenv('BASE_API_URL')
        #self.redirect_uri = os.getenv('REDIRECT_URI')
#
        #self.auth_url = os.getenv('AUTH_URL')
        #self.access_url = os.getenv('ACCESS_URL')
        self.client_id = '1fvo2c155aknlf8i37h7p6qeri'
        self.client_secret = 'oqm61c2725jpfbo2i4s18t12c0'
        self.base_api_url = 'https://api.meetup.com/gql'
        self.redirect_uri = 'https://event-collector-api.herokuapp.com/'
        self.auth_url = 'https://secure.meetup.com/oauth2/authorize'
        self.access_url = 'https://secure.meetup.com/oauth2/access'

    def get_outh_token(self):
        '''
        oauth process flow to get the token needed for querying the Meetup API with graphQL
        '''
        grant_type = 'anonymous_code'
        headers = {'Accept': 'application/json'}
        auth_params = {'client_id': self.client_id, 'response_type': grant_type, 'redirect_uri': self.redirect_uri}

        try:
            auth_response = requests.get(self.auth_url, params=auth_params, headers=headers)
        except requests.exceptions.RequestException as error:
            raise SystemExit(error)

        auth_token = auth_response.json()["code"]
        access_params = {'client_id': self.client_id,
                            'client_secret': self.client_secret,
                            'grant_type': grant_type,
                            'redirect_uri': self.redirect_uri,
                            'code': auth_token}

        try:
            access_response = requests.post(self.access_url, params=access_params, headers=headers)
        except requests.exceptions.RequestException as error:
            raise SystemExit(error)

        access_token = access_response.json()
        auth_string = 'Bearer %s' % access_token
        oauth_headers = {'Accept': 'application/json', 'Authorization': auth_string}
        self.oauth_headers = oauth_headers

    def query_meetup (self, query):
        try:
            res = requests.post(self.base_api_url, json={'query': query}, headers=self.oauth_headers)
        except requests.exceptions.RequestException as error:
            raise SystemExit(error)

        return res.json()

    def get_events_by_city(self, activity, lat, lon, radius):
        '''
        collect the events from a city specifed by their lat and lon for a special activity
        '''
        self.activity = activity
        self.lat = lat
        self.lon = lon
        self.radius = radius

        query = '''
            query {
                keywordSearch(filter: { query: "%s", lat: %s, lon: %s, radius: %s, source: EVENTS }) {
                    count
                    pageInfo {
                        endCursor
                    }
                    edges {
                        node {
                            result {
                            ... on Event {
                            title
                            description
                            priceTier
                            numberOfAllowedGuests
                            dateTime
                            timezone
                            eventUrl
                            venue {
                                name
                                address
                                city
                                state
                                postalCode
                                country
                                lat
                                lng
                            }
                            fee
                            }
                        }
                        }
                    }
                }
            }
        ''' % (self.activity, self.lat, self.lon, self.radius)

        events = self.query_meetup(query)

        return events

def main():
    meetup = Meetup()
    meetup.get_outh_token()
    events = meetup.get_events_by_city("fitness", 52.520008, 13.404954, 100)
    print(events)

if __name__ == '__main__':
    main()
