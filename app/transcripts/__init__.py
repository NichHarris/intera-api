from flask import Blueprint

transcripts = Blueprint('transcripts', __name__)

from app.transcripts import routes
from app.transcripts import controller