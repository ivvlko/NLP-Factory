from app import app
import dash
from flask import Blueprint

hn_dashboard = Blueprint('hn_dashboard', __name__, template_folder='templates')

server = app

dashApp = dash.Dash(
    __name__,
    server=server,
    url_base_pathname='/hn_dashboard/',
    assets_folder='assets'
)
dashApp.config['suppress_callback_exceptions']=True
dashApp.title = 'HN Dashboard'


from applications.hn_dashboard.callbacks import *
from applications.hn_dashboard.layout import layout
dashApp.layout = layout


@hn_dashboard.route("/hn_dashboard/")
def my_dash_app():
    return dashApp.index()
