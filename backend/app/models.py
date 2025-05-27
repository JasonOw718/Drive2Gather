from datetime import datetime
from itsdangerous.url_safe import URLSafeSerializer as serializer
from app import db, loginManager
from flask_login import UserMixin

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable= False)
    password = db.Column(db.String(60), nullable= False)
    email = db.Column(db.String(60), unique=True, nullable= False)

    def get_reset_token(self):
        s = serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_reset_token(token):
        s = serializer(app.config['SECRET_KEY'])

        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"User ('{self.username}', '{self.password}', '{self.email}')"