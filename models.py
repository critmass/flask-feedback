"""database models for flask feedback project"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):

    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    username = db.Column(
        db.String(20),
        nullable=False,

    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    email = db.Column(
        db.String(50),
        nullable=False
    )

    password = db.Column(
        db.Text,
        nullable=False
    )

    @classmethod
    def signup(cls, first_name, last_name, username, password, email):

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_pwd

        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Feedback(db.Model):

    __tablename__ = 'feedback'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
)

    content = db.Column(
        db.Text(),
        nullable=False
    )

    username = db.Column(
        db.String(20),
        db.ForeignKey('user.username', ondelete='CASCADE'),
        nullable=False
    )

    user = db.relationship("User", backref="feedback")

