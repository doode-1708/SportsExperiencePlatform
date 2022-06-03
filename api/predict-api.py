# rm
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import datetime
from datetime import date

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
    return {"greeting": f"Welcome to the Sports Experience Recommendation System"}

@app.get('/content_recommender')
def content_recommender(user_id, cosine_sim = cosine_sim, df = events_df, title_to_index = title_to_index):
    '''
    This recommender finds out 20 closest matches with a given event
    '''
# source: sk_simple_recommender.ipynb

    # calling user id from ahoy_events

    title = get_title(user_id, df = ahoy_events_df)

    idx = title_to_index[title]

    sim_scores = list(enumerate(cosine_sim[idx].todense().tolist()[0]))
    # list of set [(index, sim score), (index, sim score), ...]

    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    # Sort the list of set by sim score, index with highest similarity
    # Will be at the beginning of the list

    sim_scores = sim_scores[1:101] # top 100 events (first one is our input event so we ignore it)

    sport_indices = [i[0] for i in sim_scores] # we grab the indices of those 10 events

    df_all_recommendations = df.iloc[sport_indices][['title', 'latitude', 'longitude', 'offer_date']]

    df_date_filter = df_all_recommendations[df_all_recommendations['offer_date'] >= datetime.date.today()]

    # calculation of haversine distance for users:
    user_latitude = get_user_loc(user_id, df = users_df)['user_latitude']
    user_longitude = get_user_loc(user_id, df = users_df)['user_longitude']

    df_date_filter['user_latitude'] = user_latitude
    df_date_filter['user_longitude'] = user_longitude

    df_date_filter["distance"] = haversine_vectorized(df_date_filter.latitude, df_date_filter.longitude,
                                                      df_date_filter.user_latitude, df_date_filter.user_longitude)

    df_location_filter = df_date_filter[df_date_filter['distance'] <= 200.0]



    return df_location_filter.title
#   return user_latitude
