# Intera - An ASL/Speech to Text Faciliator & Learning Platform (API Server)

### Installation Guide

>Pre-requisite: Must be on Python version 3.8+, and python virtualenv and pip3
```
python3 -m pip install --user --upgrade pip
python3 -m pip install --user virtualenv
```

## Setup virtual environment
```
python -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Import the .env file
Import the .env file provided under the `intera-api/` directory

## Start up server
```
gunicorn --workers 4 --worker-class gevent -b 127.0.0.1:5000  app:app
```


### Updating requirements file when adding a package
After installing a new package, update the `requirements.txt` file with the content from the command `pip3 freeze > requirements.txt`

