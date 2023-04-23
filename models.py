from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()


class Resource(db.Model):
    """Resource model"""
    __tablename__ = ""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
