from app import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from db_models.hackerNewsModels import TopicLabel
import os
from flask import url_for


app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = os.urandom(24)
admin = Admin(app, template_mode='bootstrap3')
admin.add_view(ModelView(TopicLabel, db.session))
app.config['FLASK_ADMIN_SWATCH'] = 'cyborg'
