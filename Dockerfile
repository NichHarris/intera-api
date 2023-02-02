# pull official base image
FROM python:3.10-slim-buster

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /intera-app/requirements.txt
RUN pip install -r /intera-app/requirements.txt

# copy project
COPY . /intera-app/

WORKDIR /intera-app/

CMD exec gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 4 --worker-connections=1000 --reload -b :$PORT app:app
