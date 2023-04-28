from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()


class User(db.Model):
    """User model"""

# tablename to create to store the users
    __tablename__ = "users"
# model columns setup
    username = db.Column(db.String, nullable=False,
                         primary_key=True, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

# register and authenticate a user with class methods below
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return User"""
        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """ validate that user exists & password is correct.
        return user if valid; else return False
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False

    def full_name(cls):
        """return users full name"""

        return f"{cls.first_name} {cls.last_name}"


class Feedback(db.Model):
    """Feedback model"""

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String, db.ForeignKey('users.username'))

    user = db.relationship('User', backref='feedback')
