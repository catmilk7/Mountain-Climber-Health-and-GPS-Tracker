from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    full_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    
    def get_token(self, expires_sec=300):
        serial=Serializer(current_app.config['SECRET_KEY'])
        return serial.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_token(token):
        serial=Serializer(current_app.config['SECRET_KEY'])
        try:
            data = serial.loads(token, max_age=300)
            user_id = data['user_id']
        except:
            return None
        return User.query.get(user_id)