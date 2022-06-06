from flask import Blueprint

surveys_bp = Blueprint('surveys', __name__, template_folder='templates')

from . import routes