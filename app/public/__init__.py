from base64 import urlsafe_b64decode
from flask import Blueprint

public_bp = Blueprint('public', __name__, template_folder='templates', static_folder='static',url_prefix='',static_url_path='/public-static')

from . import routes