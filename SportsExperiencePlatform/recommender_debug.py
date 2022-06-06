import numpy as np
import pandas as pd
from SportsExperiencePlatform.data import connect_db, get_data, upload_file_to_gs
from SportsExperiencePlatform.utils_debug import language_translation, clean_string, haversine_vectorized, random_title, random_description
import random
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from scipy.sparse import save_npz, load_npz


BUCKET_NAME = 'wagon-817-project-sports'
STORAGE_LOCATION = 'models/recommender/model_cosine_sim'



class Recommender():
    def __init__(self):
        print("initalizing the recommender")

    # translation

    # creating title and description soup
    def create_soup(self, x):
        soup = (" ".join(x["random_title"]) + " " + " ".join(x["random_description"])).split()
        random.shuffle(soup)
        return ' '.join(soup)

    def get_transformed_df(self):

        # connect with db
        conn = connect_db()

        if conn:
            self.users_df, self.events_df, self.ahoy_events_df = get_data(conn)

        #translation
        self.events_df['translated_title'] = self.events_df['title'].apply(lambda x: language_translation(x))
        self.events_df['translated_description'] = self.events_df['description'].apply(lambda x: language_translation(x))
#
        ##cleaning
        self.events_df['clean_description'] = self.events_df['translated_description'].apply(lambda x: clean_string(x))
        self.events_df['clean_title'] = self.events_df['translated_title'].apply(lambda x: clean_string(x))
#
        ##randomizing title and description
        self.events_df['random_title'] = self.events_df['clean_title'].apply(lambda x: random_title(x))
        self.events_df['random_description'] = self.events_df['clean_description'].apply(lambda x: random_description(x))
        self.events_df['soup'] = self.events_df.apply(self.create_soup, axis = 1)

        # return self.users_df, self.events_df, self.ahoy_events_df
        return self.events_df.head()

    def get_event_id(self, user_id):
        ''' this finction grabs the title of an event used by an user from ahoy_events dataset'''

        self.user_id = user_id
        event_id = self.ahoy_events_df[self.ahoy_events_df['user_id']== self.user_id].iloc[-1].properties['offer']
        # now we get the title of the event
        #event_id = events_df[events_df['id']==event_idx].title

        return event_id

    def get_user_loc(self, user_id):
        ''' this function grabs the location of an user from ahoy_events dataset'''

        users_idx = self.users_df[self.users_df['id']== user_id]
        # now we get the user's latitude and longitude

        location_dict = {'user_latitude' : float(users_idx.latitude.values),

                        'user_longitude' : float(users_idx.longitude.values)
                            }

        return location_dict

    def cosine_similarity(self):
        tfidf = TfidfVectorizer(stop_words="english")
        tfidf_matrix = tfidf.fit_transform(self.events_df["soup"])
        cosine_sim = tfidf_matrix.dot(tfidf_matrix.T)

        return cosine_sim

if __name__ == '__main__':
    trainer = Recommender()
    print(trainer.get_transformed_df())
    # get_event_id(user_id)
    # get_user_loc(user_id)
    # cosine_similarity()





##previous functions

# def remove_punctuation(text):
#     for s in text:
#         if s in string.punctuation:
#             text = text.replace(s, '')

#     return text

# def lower_text(text):
#     return text.lower()

# def remove_numbers(text):
#     return ''.join(word for word in text  if not word.isdigit())

# def remove_stop_words(text, language='english'):
#     stop_words = set(stopwords.words(language))
#     word_tokens = word_tokenize(text)

#     return ' '.join([w for w in word_tokens if not w in stop_words])

# def lemmatize_text(text):
#     lemmatizer = WordNetLemmatizer()

#     return ' '.join([lemmatizer.lemmatize(word) for word in text.split(' ')])

# conn = connect_db()

# if conn:
#     users_df, events_df = get_data(conn)

# events_df['description_punct'] = events_df.description.apply(remove_punctuation)
# events_df['description_lower'] = events_df.description_punct.apply(lower_text)
# events_df['description_numbers'] = events_df.description_lower.apply(remove_numbers)
# events_df['description_stopwords'] = events_df.description_numbers.apply(remove_stop_words, language='english')
# events_df['description_lemmatize'] = events_df.description_stopwords.apply(lemmatize_text)


# tfidf = TfidfVectorizer(stop_words="english")
# tfidf_matrix = tfidf.fit_transform(events_df["description_lemmatize"])

# cosine_sim = tfidf_matrix.dot(tfidf_matrix.T)

# client = storage.Client()
# bucket = client.bucket(BUCKET_NAME)
# blob = bucket.blob(STORAGE_LOCATION)
# save_npz("model_cosine_sim", cosine_sim)
# blob.upload_from_filename('model_cosine_sim.npz')
