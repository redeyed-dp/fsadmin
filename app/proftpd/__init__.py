from flask import Blueprint

bp = Blueprint('proftpd', __name__, template_folder='templates')

from app.proftpd import views