from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from . import login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password_secure = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    reviews = db.relationship('Review', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'User {self.username}'

    @property
    def password(self):
        return AttributeError('You cannot read the password')

    @password.setter
    def password(self, password):
        self.password_secure = generate_password_hash(password, method='sha256', salt_length=8)

    def verify_password(self, password):
        return check_password_hash(self.password_secure, password)


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'Role {self.name}'


class Movie:
    """
    Movie class to define Movie Objects
    """

    def __init__(self, movie_id, title, overview, poster, vote_average, vote_count):
        self.id = movie_id
        self.title = title
        self.overview = overview
        self.poster = 'https://image.tmdb.org/t/p/w500/' + poster
        self.vote_average = vote_average
        self.vote_count = vote_count


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)
    movie_title = db.Column(db.String)
    image_path = db.Column(db.String)
    movie_review = db.Column(db.String)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save_review(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_reviews(cls, id):
        reviews = Review.query.filter_by(movie_id=id).all()
        return reviews
