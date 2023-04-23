from app import app
from models import db, Resource

db.drop_all()
db.create_all()

r1 = Resource(name="Hello")
