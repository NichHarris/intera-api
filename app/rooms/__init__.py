from flask import Blueprint

rooms = Blueprint('rooms', __name__)

from app.rooms import routes
from app.rooms import controller