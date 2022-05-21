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

        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.base_api_url = os.getenv('BASE_API_URL')
        self.redirect_uri = os.getenv('REDIRECT_URI')

        self.auth_url = os.getenv('AUTH_URL')
        self.access_url = os.getenv('ACCESS_URL')
        self.default_pagination = 10

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
        oauth_headers = {'Accept': 'application/json', 'Authorization': auth_string, "Accept-Language": "en-US"}
        self.oauth_headers = oauth_headers

    def query_meetup (self, query):
        try:
            res = requests.post(self.base_api_url, json={'query': query}, headers=self.oauth_headers)
        except requests.exceptions.RequestException as error:
            raise SystemExit(error)

        return res.json()

    def get_events_by_city(self, activity, lat, lon, radius, **kwargs):
        '''
        collect the events from a city specifed by their lat and lon for a special activity
        '''
        self.activity = activity
        self.lat = lat
        self.lon = lon
        self.radius = radius

        pagination_string = ""
        if 'PageCursor' in kwargs.keys():
            page_cursor = kwargs['PageCursor']
            pagination_string = f'first: {str(self.default_pagination)}, after: "{page_cursor}"'
        else:
            pagination_string = f"first: {str(self.default_pagination)}"

        query = '''
            query {
                keywordSearch(input: {%s}, filter: { query: "%s", lat: %s, lon: %s, radius: %s, source: EVENTS }) {
                    count
                    pageInfo {
                        hasNextPage
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
                            imageUrl
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
        ''' % (pagination_string, self.activity, self.lat, self.lon, self.radius)

        events = self.query_meetup(query)

        return events

def main():
    result = []
    hasNextPage = False
    meetup = MeetupQL()
    meetup.get_outh_token()
    events = meetup.get_events_by_city("fitness", 52.520008, 13.404954, 100)
    hasNextPage = events['data']['keywordSearch']['pageInfo']['hasNextPage']

    for event in events['data']['keywordSearch']['edges']:
        result.append(event['node']['result'])

    while (hasNextPage):
        events = meetup.get_events_by_city("fitness", 52.520008, 13.404954, 100, PageCursor=events['data']['keywordSearch']['pageInfo']['endCursor'])
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

    print(event_info)

if __name__ == '__main__':
    main()
