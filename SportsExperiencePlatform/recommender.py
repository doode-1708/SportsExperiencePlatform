import numpy as np
import pandas as pd
from data import connect_db, get_data
from utils_sk import language_translation, clean_string
from utils_sk import haversine_vectorized
from utils_sk import truncate_string
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import save_npz, load_npz
from google.cloud import storage


BUCKET_NAME = 'wagon-817-project-sports'
STORAGE_LOCATION = 'models/recommender/model_cosine_sim'


class Recommender():
    def __init__(self):


    # translation

        def get_transformed_df():

            # connect with db
            conn = connect_db()

            if conn:
                self.users_df, self.events_df, self.ahoy_events_df = get_data(conn)


            #cleaning
            self.events_df['clean_description'] = self.events_df['description'].apply(lambda x: clean_string(x))
            self.events_df['clean_title'] = self.events_df['title'].apply(lambda x: clean_string(x))

            #combining title and description
            self.events_df['combined'] = self.events_df['clean_title'] + events_df['clean_description']

            # pruning out extra descriptions
            self.events_df['combined_pruned'] = self.events_df['combined'].apply(lambda x: truncate_string(x))

            #translate pruned string
            self.events_df['translated'] = self.events_df['combined_pruned'].apply(lambda x: language_translation(x))

            tfidf = TfidfVectorizer(stop_words="english")
            tfidf_matrix = tfidf.fit_transform(self.events_df["translated"])
            cosine_sim = tfidf_matrix.dot(tfidf_matrix.T)

            # return cosine_sim, self.users_df, self.ahoy_events_df
            print('alles gut')

        def get_event_id(user_id):
            ''' this finction grabs the title of an event used by an user from ahoy_events dataset'''

            self.user_id = user_id
            event_id = self.ahoy_events_df[self.ahoy_events_df['user_id']== self.user_id].iloc[-1].properties['offer']
            # now we get the id of the event

            return event_id

        def get_user_loc(user_id):
            ''' this function grabs the location of an user from ahoy_events dataset'''

            users_idx = self.users_df[self.users_df['id']== user_id]
            # now we get the user's latitude and longitude

            location_dict = {'user_latitude' : float(users_idx.latitude.values),

                            'user_longitude' : float(users_idx.longitude.values)
                                }

            return location_dict



        if __name__ == '__main__':
            trainer = Recommender()
            print('alles gut')
            # get_event_id(user_id)
            # get_user_loc(user_id)
            # cosine_similarity()


# client = storage.Client()
# bucket = client.bucket(BUCKET_NAME)
# blob = bucket.blob(STORAGE_LOCATION)
# save_npz("model_cosine_sim", cosine_sim)
# blob.upload_from_filename('model_cosine_sim.npz')
