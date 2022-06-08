# roberta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from SportsExperiencePlatform.predict import content_recommender
# from SportsExperiencePlatform.recommender import training (to be added)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# loading cosine_sim get model from gs
storage_location = f'{STORAGE_LOCATION}/model_cosine_sim.npz'
blob = client.blob(storage_location)
blob.download_to_filename('model_cosine_sim.npz')
print("=> model downloaded from storage")
model = load_npz('model_cosine_sim.npz')

# df will work when training is added to SportsExperiencePlatform.recommender (line 4)
# df = recommender.training.get_transformed_df()[1]


@app.get("/")
def index():
    return {"greeting": f"Welcome to the Sports Experience Recommendation System"}

@app.get('/recommender')
def predict(user_id):
    return content_recommender(user_id, model, df)




# ===============================================
# ***************** NEXT STEPS: *****************
# ===============================================
#
# test it


# Daniel's instructions:
# file: predict-api.py
#  --> fastapi
#  --> import from data google functions, get model, do the recommendation
#  --> import predicting functions from recommender.py
#       --> get_title, content_recommender, haversine_vectorized, get_user_loc
