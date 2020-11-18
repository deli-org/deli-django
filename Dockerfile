#base image
FROM python:3.8

COPY ./requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /code
COPY . /code/

#install psycopg2
RUN apt update \
  && apt install -y libpq-dev gcc

RUN pip install psycopg2
RUN apt-get -y install zsh

#run gunicorn
CMD gunicorn deli.wsgi.application --bind 0.0.0.0:$PORT

