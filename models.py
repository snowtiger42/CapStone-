from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager


db = SQLAlchemy()
login = LoginManager()


class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))


class EventModel(db.Model):
    __tablename__ ='user_events'

    username = db.Column(db.String(80), primary_key=True, nullable=False)
    events = db.Column(db.BLOB, nullable=False)

    def events_json(self):
        return self.events
