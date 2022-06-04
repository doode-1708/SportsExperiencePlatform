from email import message
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import storage
from scipy.sparse import load_npz
from SportsExperiencePlatform.utils import haversine_vectorized
import pandas as pd
from datetime import date
import datetime
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/credentials.json"

BUCKET_NAME = 'wagon-817-project-sports'
STORAGE_LOCATION = 'models/recommender'

def get_title(user_id, ahoy_events_df, events_df):
    ''' this function grabs the title of an event used by an user from ahoy_events dataset'''

    #event_idx = ahoy_events_df[ahoy_events_df['user_id']== user_id].iloc[0].properties['offer']
    # now we get the title of the event
    event_idx = 1375
    title = events_df[events_df['id']==event_idx].title

    return title

def get_user_loc(user_id, users_df):
    ''' this finction grabs the location of an user from ahoy_events dataset'''

    users_idx = users_df[users_df['id']== user_id]
    # now we get the user's latitude and longitude

    location_dict = {'user_latitude' : float(users_idx.latitude.values),

                     'user_longitude' : float(users_idx.longitude.values)
                        }

    return location_dict


def content_recommender(user_id, cosine_sim, events_df, users_df, ahoy_events_df, title_to_index):
    '''This recommender finds out 20 closest matches with a given event'''

    #calling user id from ahoy_events

    title = get_title(user_id, ahoy_events_df, events_df)

    idx = title_to_index[title]

    sim_scores = list(enumerate(cosine_sim[idx].todense().tolist()[0]))
    # list of set [(index, sim score), (index, sim score), ...]

    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    # Sort the list of set by sim score, index with highest simlirarity
    # Will be at the beginning of the list

    sim_scores = sim_scores[1:101] # top 100 events (first one is our input events so we ignore it)

    sport_indices = [i[0] for i in sim_scores] # we grab the indices of those 10 events

    df_all_recommendations = events_df.iloc[sport_indices][['id','title', 'latitude', 'longitude', 'offer_date']]

    #df_date_filter = df_all_recommendations.copy() #[df_all_recommendations['offer_date'] >= datetime.date.today()]
#
    ##calcullation of haversine distance for users:
    #user_latitude = get_user_loc(user_id, users_df)['user_latitude']
    #user_longitude = get_user_loc(user_id, users_df)['user_longitude']
#
    #df_date_filter['user_latitude'] = user_latitude
    #df_date_filter['user_longitude'] = user_longitude
#
    #df_date_filter["distance"] = haversine_vectorized(df_date_filter.latitude, df_date_filter.longitude,
    #                                                  df_date_filter.user_latitude, df_date_filter.user_longitude)
#
    #df_location_filter = df_date_filter[df_date_filter['distance'] <= 200.0]
#
#
    return df_all_recommendations.id
    #return df_location_filter.title
#     return user_latitude

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

client = storage.Client().bucket(BUCKET_NAME)

# get model from gs
storage_location = f'{STORAGE_LOCATION}/model_cosine_sim.npz'
blob = client.blob(storage_location)
blob.download_to_filename('model_cosine_sim.npz')
print("=> model downloaded from storage")
model = load_npz('model_cosine_sim.npz')

storage_location_ahoy = f'{STORAGE_LOCATION}/ahoy_events_df.csv'
blob = client.blob(storage_location_ahoy)
blob.download_to_filename('ahoy_events_df.csv')
ahoy_events_df = pd.read_csv('ahoy_events_df.csv')

storage_location_events = f'{STORAGE_LOCATION}/events_df.csv'
blob = client.blob(storage_location_events)
blob.download_to_filename('events_df.csv')
events_df = pd.read_csv('events_df.csv')

storage_location_users = f'{STORAGE_LOCATION}/users_df.csv'
blob = client.blob(storage_location_users)
blob.download_to_filename('users_df.csv')
users_df = pd.read_csv('users_df.csv')

#print(ahoy_events_df[ahoy_events_df['user_id']== 59].iloc[0].properties['offer'])

title_to_index = pd.Series(events_df.index, index = events_df["title"]).drop_duplicates()

@app.get("/")
def index():
    return {"greeting": f"Welcome to the Sports Experience Recommendation System"}

@app.get("/recommender")
def recommender(user_id):
    id = int(user_id)
    results = content_recommender(id, model, events_df, users_df, ahoy_events_df, title_to_index)

    #print(results.info())
    return results.tolist()
