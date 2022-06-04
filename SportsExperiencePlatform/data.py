import psycopg2
from dotenv import load_dotenv, find_dotenv
import os
import pandas as pd
from scipy.sparse import load_npz, save_npz
from SportsExperiencePlatform.params import BUCKET_NAME, STORAGE_LOCATION, MODEL_FILE_NAME, EVENTS_FILE_NAME
from google.cloud import storage

def connect_db():
    env_path = find_dotenv()
    load_dotenv(env_path)
    POSTGRE_HOST = os.getenv('POSTGRE_HOST')
    POSTGRE_DATABASE = os.getenv('POSTGRE_DATABASE')
    POSTGRE_DB_USER = os.getenv('POSTGRE_DB_USER')
    POSTGRE_DB_PW = os.getenv('POSTGRE_DB_PW')

    try:
        conn = psycopg2.connect(
        host=POSTGRE_HOST,
        database=POSTGRE_DATABASE,
        user=POSTGRE_DB_USER,
        password=POSTGRE_DB_PW)
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    return conn

def get_data(conn):
    query_users = "select * from users"
    query_events = "select * from offers"
    query_ahoy_events = "select * from ahoy_events"
    df_users = pd.read_sql(query_users, conn)
    df_events = pd.read_sql(query_events, conn)
    df_ahoy_events = pd.read_sql(query_ahoy_events, conn)

    conn.close()

    return (df_users, df_events, df_ahoy_events)

def download_file_from_gs(filename):
    download_file = None
    client = storage.Client().bucket(BUCKET_NAME)

    storage_location = f'{STORAGE_LOCATION}/{filename}'
    blob = client.blob(storage_location)
    blob.download_to_filename(filename)

    if filename.split('.')[1] == 'npz':
        download_file = load_npz(filename)
    elif filename.split('.')[1] == 'csv':
        download_file = pd.read_csv(filename)

    return download_file

def upload_file_to_gs(filename, **kwargs):
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(f'{STORAGE_LOCATION}/{filename}')

    if 'model' in kwargs.keys():
        save_npz(filename, kwargs['model'])

    blob.upload_from_filename(filename)

def main():
    conn = connect_db()
    df_users, df_events, df_ahoy_events = get_data(conn)
    print(df_users.shape, df_events.shape)
    model = download_file_from_gs(MODEL_FILE_NAME)
    events_df = download_file_from_gs(EVENTS_FILE_NAME)
    print(model.shape)
    print(events_df.head())
    upload_file_to_gs(EVENTS_FILE_NAME)
    upload_file_to_gs(MODEL_FILE_NAME, model=model)

if __name__ == '__main__':
    main()
