from flask import Blueprint

neural_net = Blueprint('neural_net', __name__)

from app.neural_net import controller
from app.neural_net import routes
