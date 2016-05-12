from flask import Blueprint

topology = Blueprint('topology', __name__, template_folder='templates')
from . import views
