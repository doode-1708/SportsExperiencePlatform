FROM python:3.8.12-buster
COPY credentials.json /credentials.json
COPY SportsExperiencePlatform /SportsExperiencePlatform
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD  uvicorn SportsExperiencePlatform.dirty_predict:app --host 0.0.0.0 --port $PORT
