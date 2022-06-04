# roberta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from SportsExperiencePlatform.predict import content_recommender
# import datetime
# from datetime import date

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

@app.get('/recommender')
def predict(user_id):
    return content_recommender(user_id, cosine_sim, df)


# (user_id, cosine_sim = cosine_sim, df = events_df)

# ===============================================
# ***************** NEXT STEPS: *****************
# ===============================================
#
# how to load: cosine_sim:
# get model from gs
# storage_location = f'{STORAGE_LOCATION}/model_cosine_sim.npz'
# blob = client.blob(storage_location)
# blob.download_to_filename('model_cosine_sim.npz')
# print("=> model downloaded from storage")
# model = load_npz('model_cosine_sim.npz')
#
# check # data.py
#
# , df, title_to_index
# test it
