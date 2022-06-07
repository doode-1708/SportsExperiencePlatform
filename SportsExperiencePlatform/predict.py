from email import message
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import storage
from scipy.sparse import load_npz
from data import connect_db, get_data
from recommender_sk import get_transformed_df
from recommender_sk import get_event_id
from recommender_sk import get_event_id
from recommender_sk import get_user_loc
from utils_sk import haversine_vectorized
import datetime


import pandas as pd

BUCKET_NAME = 'wagon-817-project-sports'
STORAGE_LOCATION = 'models/recommender'

client = storage.Client().bucket(BUCKET_NAME)

# get model from gs
storage_location = '{}/{}'.format(
    STORAGE_LOCATION,
    'model_cosine_sim')
blob = client.blob(storage_location)
blob.download_to_filename('model_cosine_sim.npz')
print("=> model downloaded from storage")
model = load_npz('model_cosine_sim.npz')


events_df, users_df, ahoy_events_df = get_transformed_df()

def content_recommender(user_id, cosine_sim = model, events_df):
    '''This recommender finds out 100 closest matches with a given event'''

    #calling user id from ahoy_events


    event_idx = events_df[events_df['id']== get_event_id(user_id)].index


    sim_scores = list(enumerate(cosine_sim[event_idx].todense().tolist()[0]))
    # list of set [(index, sim score), (index, sim score), ...]

    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    # Sort the list of set by sim score, index with highest simlirarity
    # Will be at the beginning of the list

    sim_scores = sim_scores[1:101] # top 100 events (first one is our input events so we ignore it)

    sport_indices = [i[0] for i in sim_scores] # we grab the indices of those 10 events

    df_all_recommendations = df.iloc[sport_indices][[ 'id','title', 'latitude', 'longitude', 'offer_date']]

    df_date_filter = df_all_recommendations[df_all_recommendations['offer_date'] >= datetime.date.today()]

    #calcullation of haversine distance for users:
    user_latitude = get_user_loc(user_id, df = users_df)['user_latitude']
    user_longitude = get_user_loc(user_id, df = users_df)['user_longitude']

    df_date_filter['user_latitude'] = user_latitude
    df_date_filter['user_longitude'] = user_longitude

    df_date_filter["distance"] = haversine_vectorized(df_date_filter.latitude, df_date_filter.longitude,
                                                      df_date_filter.user_latitude, df_date_filter.user_longitude)

    df_location_filter = df_date_filter[df_date_filter['distance'] <= 200.0]



    return df_location_filter.to_dict()



# def content_recommender(title, cosine_sim, df, title_to_index):
#     idx = title_to_index[title]

#     sim_scores = list(enumerate(cosine_sim[idx].todense().tolist()[0]))
#     # list of set [(index, sim score), (index, sim score), ...]

#     sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
#     # Sort the list of set by sim score, index with highest simlirarity
#     # Will be at the beginning of the list

#     sim_scores = sim_scores[1:11] # top 10 events (first one is our input events so we ignore it)

#     sport_indices = [i[0] for i in sim_scores] # we grab the indices of those 10 events

#     return df["title"].iloc[sport_indices]

# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )

# client = storage.Client().bucket(BUCKET_NAME)

# # get model from gs
# storage_location = '{}/{}'.format(
#     STORAGE_LOCATION,
#     'model_cosine_sim')
# blob = client.blob(storage_location)
# blob.download_to_filename('model_cosine_sim.npz')
# print("=> model downloaded from storage")
# model = load_npz('model_cosine_sim.npz')

# '''
#     very ugly, just for demo purpose
#     we have to think about how to save the event titles to
# '''

# conn = connect_db()

# if conn:
#     users_df, events_df = get_data(conn)
# title_to_index = pd.Series(events_df.index, index = events_df["title"]).drop_duplicates()

# @app.get("/")
# def index():
#     return {"greeting": f"Welcome to the Sports Experience Recommendation System"}

# @app.get("/recommender")
# def query_meetup(title):
#     results = content_recommender(title, model, events_df, title_to_index)

#     return results.to_dict()
