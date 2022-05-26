import numpy as np
import pandas as pd
from SportsExperiencePlatform.data import connect_db, get_data
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from scipy.sparse import save_npz
from google.cloud import storage

BUCKET_NAME = 'wagon-817-project-sports'
STORAGE_LOCATION = 'models/recommender/model_cosine_sim'

def remove_punctuation(text):
    for s in text:
        if s in string.punctuation:
            text = text.replace(s, '')

    return text

def lower_text(text):
    return text.lower()

def remove_numbers(text):
    return ''.join(word for word in text  if not word.isdigit())

def remove_stop_words(text, language='english'):
    stop_words = set(stopwords.words(language))
    word_tokens = word_tokenize(text)

    return ' '.join([w for w in word_tokens if not w in stop_words])

def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()

    return ' '.join([lemmatizer.lemmatize(word) for word in text.split(' ')])

conn = connect_db()

if conn:
    users_df, events_df = get_data(conn)

events_df['description_punct'] = events_df.description.apply(remove_punctuation)
events_df['description_lower'] = events_df.description_punct.apply(lower_text)
events_df['description_numbers'] = events_df.description_lower.apply(remove_numbers)
events_df['description_stopwords'] = events_df.description_numbers.apply(remove_stop_words, language='english')
events_df['description_lemmatize'] = events_df.description_stopwords.apply(lemmatize_text)


tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(events_df["description_lemmatize"])

cosine_sim = tfidf_matrix.dot(tfidf_matrix.T)

client = storage.Client()
bucket = client.bucket(BUCKET_NAME)
blob = bucket.blob(STORAGE_LOCATION)
save_npz("model_cosine_sim", cosine_sim)
blob.upload_from_filename('model_cosine_sim.npz')
