from functools import wraps

from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey<3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from models import User, Ad, Course, FavoriteCourse,FavoriteAd





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))