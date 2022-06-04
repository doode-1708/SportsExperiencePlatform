import numpy as np
from googletrans import Translator
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import random

def language_translation(string):

        self.string = string
        translator = Translator()
        if translator.detect(self.string).lang != 'en':
            result = translator.translate(self.string)
            return result.text
        else:
            return string

def clean_string(text,stem="None"):
    8# load spacy
    nlp = spacy.load('en_core_web_sm')

    final_string = ""

    # make lower
    text = text.lower()

    # remove http
    text = re.sub(r"http.*\.[a-z]{2,3}","",text)

    # remove www
    text = re.sub(r"www.*\.[a-z]{2,3}","",text)

    # remove line breaks
    text = re.sub(r'\n','',text)

    # remove puncuation
    translator = str.maketrans('','',string.punctuation)
    text = text.translate(translator)

    # remove stop words
    text = text.split()
    useless_words = nltk.corpus.stopwords.words("english")
    text_filtered = [word for word in text if not word in useless_words]

    # remove numbers
    text_filtered = [re.sub(r'\w*\d\w*','',w) for w in text_filtered]

    # stem or lemmatize
    if stem == 'Stem':
        stemmer = PorterStemmer()
        text_stemmed = [stemmer.stem(y) for y in text_filtered]
    elif stem == 'Lem':
        lem = WordNetLemmatizer()
        text_stemmed = [lem.lemmatize(y) for y in text_filtered]
    elif stem == 'Spacy':
        text_filtered = nlp(' '.join(text_filtered))
        text_stemmed = [y.lemma_ for y in text_filtered]
    else:
        text_stemmed = text_filtered

    final_string = ' '.join(text_stemmed)

    return final_string

# create randomised title
def random_title(x):
    names = list(x.split())
    random.shuffle(names)
    if len(names) > 5:
        names = names[:5]

# create randomised description
def random_description(x):
    names = list(x.split())
    random.shuffle(names)
    if len(names) > 200:
        names = names[:200]


    return names






def haversine_vectorized(user_lat,
                         user_lon,
                         event_lat,
                         event_lon):
    """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees).
        Vectorized version of the haversine distance for pandas df
        Computes distance in kms
    """

    lat_1_rad, lon_1_rad = np.radians(user_lat), np.radians(user_lon)
    lat_2_rad, lon_2_rad = np.radians(event_lat), np.radians(event_lon)
    dlon = lon_2_rad - lon_1_rad
    dlat = lat_2_rad - lat_1_rad

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat_1_rad) * np.cos(lat_2_rad) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return 6371 * c
