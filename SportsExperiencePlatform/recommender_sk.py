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



# class Recommender():
#     def __init__(self):
#         print("initalizing the recommender")

#     # translation

    # creating title and description soup

def get_transformed_df():

    # connect with db
    conn = connect_db()

    if conn:
        users_df, events_df, ahoy_events_df = get_data(conn)

    #cleaning
        events_df['clean_description'] = events_df['description'].apply(lambda x: clean_string(x))
        events_df['clean_title'] = events_df['title'].apply(lambda x: clean_string(x))

        #combining title and description
        events_df['combined'] = events_df['clean_title'] + events_df['clean_description']

        # pruning out extra descriptions
        events_df['combined_pruned'] = events_df['combined'].apply(lambda x: truncate_string(x))

        #translate pruned string
        events_df['translated'] = events_df['combined_pruned'].apply(lambda x: language_translation(x))

        #calculate cosine similarity
        tfidf = TfidfVectorizer(stop_words="english")
        tfidf_matrix = tfidf.fit_transform(events_df["translated"])
        cosine_sim = tfidf_matrix.dot(tfidf_matrix.T)

        return cosine_sim, events_df, users_df, ahoy_events_df
        # print('done')

def get_event_id(user_id, ahoy_events_df):
    ''' this finction grabs the title of an event used by an user from ahoy_events dataset'''

    user_id = user_id
    event_id = ahoy_events_df[ahoy_events_df['user_id']== user_id].iloc[-1].properties['offer']
    # now we get the title of the event
    #event_id = events_df[events_df['id']==event_idx].title

    return event_id

def get_user_loc(user_id, users_df):
    ''' this function grabs the location of an user from ahoy_events dataset'''

    users_idx = users_df[users_df['id']== user_id]
    # now we get the user's latitude and longitude

    location_dict = {'user_latitude' : float(users_idx.latitude.values),

                    'user_longitude' : float(users_idx.longitude.values)
                        }

    return location_dict


# if __name__ == '__main__':
#     trainer = Recommender()
#     print(trainer.get_transformed_df())
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
