import psycopg2
from dotenv import load_dotenv, find_dotenv
import os
import pandas as pd
import streamlit as st

env_path = find_dotenv()
load_dotenv(env_path)
POSTGRE_HOST = os.getenv('POSTGRE_HOST')
POSTGRE_DATABASE = os.getenv('POSTGRE_DATABASE')
POSTGRE_DB_USER = os.getenv('POSTGRE_DB_USER')
POSTGRE_DB_PW = os.getenv('POSTGRE_DB_PW')

conn = psycopg2.connect(
    host=POSTGRE_HOST,
    database=POSTGRE_DATABASE,
    user=POSTGRE_DB_USER,
    password=POSTGRE_DB_PW)

query = "select version()"
df = pd.read_sql(query, conn)

st.write(df)

conn.close()
