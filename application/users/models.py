import base64
from datetime import datetime, timedelta
from hashlib import md5
import os
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash
from application.extensions import db, lm
import jwt
from application.models import PaginatedAPIMixin


class User(UserMixin, PaginatedAPIMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    token = db.Column(db.String(32), unique=True)
    token_expiration = db.Column(db.DateTime)
    about_me = db.Column(db.String(128))

    def __init__(self, username, email, password):
        self.username = username
        self.password = password
        self.email = email
        self.token = self.get_token()

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])


    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def save(self):

        # inject self into db session
        db.session.add ( self )

        # commit change and save the object
        db.session.commit( )

        return self

    # Set an empty string to null for username field => https://stackoverflow.com/a/57294872
    @validates('username')
    def empty_string_to_null(self, key, value):
        if isinstance(value, str) and value == '':
            return None
        else:
            return value


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
