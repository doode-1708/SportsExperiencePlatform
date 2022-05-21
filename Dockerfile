FROM python:3.8.12-buster
COPY SportsExperiencePlatform /SportsExperiencePlatform
COPY requirements.txt /requirements.txt
COPY .env /.env
COPY setup.sh /setup.sh
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD  sh setup.sh && streamlit run SportsExperiencePlatform/data.py
