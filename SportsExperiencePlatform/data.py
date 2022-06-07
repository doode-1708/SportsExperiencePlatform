import psycopg2
from dotenv import load_dotenv, find_dotenv
import os
import pandas as pd

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

def main():
    conn = connect_db()
    df_users, df_events, df_ahoy_events = get_data(conn)
    print(df_users.shape, df_events.shape, df_ahoy_events.shape)

if __name__ == '__main__':
    main()
