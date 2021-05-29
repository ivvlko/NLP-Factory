import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://" \
                                        f"{os.environ.get('DB_USER')}:" \
                                        f"{os.environ.get('DB_PASS')}" \
                                        f"@localhost:{os.environ.get('DB_PORT')}" \
                                        f"/{os.environ.get('DB_NAME')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)


@login_manager.user_loader
def load_user(user_id):
    return User.id


db = SQLAlchemy(app)
migrate = Migrate(app, db)

from db_models.user import User
from db_models.admin import admin
from db_models.api import api
from applications.home.home import home_page
from applications.hackernews_nlp.routes import news_topics_labelling
from applications.hn_dashboard.dashapp import hn_dashboard
from applications.auth.routes import auth

app.register_blueprint(auth)
app.register_blueprint(home_page)
app.register_blueprint(news_topics_labelling)
app.register_blueprint(hn_dashboard)


if __name__ == '__main__':
    app.run(debug=False)
