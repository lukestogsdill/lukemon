from flask import Blueprint

main = Blueprint('main', __name__, template_folder='main_templates', url_prefix='/')

from . import routes