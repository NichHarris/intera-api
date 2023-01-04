from flask import Blueprint

practice_module = Blueprint('practice_module', __name__)

from app.practice_module import routes
from app.practice_module import controller