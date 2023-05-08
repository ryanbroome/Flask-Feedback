from app import app
from models import db, User, Feedback

db.drop_all()
db.create_all()

# ? create instances of user and hash PW by using Class method .register to seed db
u1 = User.register(
    username="userONE",
    password="password",
    email="userONE@gmail.com",
    first_name="user",
    last_name="ONE"
)

u2 = User.register(
    username="userTWO",
    password="password",
    email="userTWO@gmail.com",
    first_name="user",
    last_name="TWO"
)

# ? register user instances to hash the pw's using flask_bcrypt before sending to db
ryan = User.register('ryanbroome', 'password',
                     'ryanbroome@gmail.com', 'Ryan', 'Broome')

f1 = Feedback(title="first userONE feedback",
              content="I am userONE and i post  content", username=u1.username)
f2 = Feedback(title="first userTWO feedback",
              content="I am userTWO and this is my content that I like to post", username=u2.username)


# ? send to db
db.session.add_all([u1, u2, ryan])
db.session.commit()

db.session.add_all([f1, f2])
db.session.commit()
