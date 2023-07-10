from flask import Flask, render_template
from flask_login import LoginManager
from dotenv import load_dotenv
import config
import os

#creat app object
app = Flask(__name__)

#env configuration
APP_ROOT = os.path.join(os.path.dirname(__file__), "..")
dotenv_path = os.path.join(APP_ROOT, ".env")
load_dotenv(dotenv_path)
app.config.from_object('config.settings.' + os.environ.get('ENV'))

#database
from app.models import db, users
db.create_all()
db.session.commit()

#login
from app.models.users import User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#error page
@app.errorhandler(404)
def not_found(error):
    title = 'page not found'
    return render_template('errors/404.html', title=title), 404


#import blueprints
from app.views.home import home as home_blueprint
from app.views.auth import auth as auth_blueprint

#register blueprints
app.register_blueprint(home_blueprint)
app.register_blueprint(auth_blueprint)