from flask import Blueprint

account = Blueprint('account', __name__, template_folder='templates')
from . import views