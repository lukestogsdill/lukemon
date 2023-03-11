from flask import Blueprint

team = Blueprint('team', __name__, template_folder ='team_templates', url_prefix='/team')

from . import routes