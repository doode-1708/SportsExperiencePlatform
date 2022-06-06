from email import message
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from SportsExperiencePlatform.params import BUCKET_NAME, STORAGE_LOCATION
from google.cloud import storage
import json

if not os.uname()[1] == 'doodebook':
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/credentials.json"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

client = storage.Client().bucket(BUCKET_NAME)
storage_location = f'{STORAGE_LOCATION}/recommender.json'
blob = client.blob(storage_location)
blob.download_to_filename('recommender.json')

with open('recommender.json', 'r') as fp:
    recommendation = json.load(fp)

@app.get("/")
def index():
    return {"greeting": f"Welcome to the Sports Experience Recommendation System"}

@app.get("/recommender")
def recommender(user_id):

    return recommendation[user_id]
