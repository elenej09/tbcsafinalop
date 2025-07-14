from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


from extensions import db



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    birthday = db.Column(db.Date)
    gender = db.Column(db.String(10))
    country = db.Column(db.String(30))
    role = db.Column(db.String(10), default="guest")
    ads = db.relationship('Ad', backref='author', lazy=True)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Ad {self.title}>'

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    image_file = db.Column(db.String, default="default.jpg")
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Course {self.title}>'



class FavoriteCourse(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    course_id=db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<FavoriteCourse user={self.user_id}   course={self.course_id}>'


class FavoriteAd(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    ad_id=db.Column(db.Integer, db.ForeignKey('ad.id'), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<FavoriteCourse user={self.user_id}   ad={self.ad_id}>'
