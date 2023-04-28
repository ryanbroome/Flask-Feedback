from app import app
from models import db, User, Feedback

db.drop_all()
db.create_all()

# ? create instances of user and hash PW by using Class method .register to seed db
u1 = User.register(
    username="eddymunsta",
    password="password",
    email="eddymunsta@gmail.com",
    first_name="Eddy",
    last_name="Munsta"
)

u2 = User.register(
    username="roman",
    password="password",
    email="roman@gmail.com",
    first_name="Roman",
    last_name="Munsta"
)

# ? register user instances to hash the pw's using flask_bcrypt before sending to db
ryan = User.register('ryanb', 'password', 'ryan@gmail.com', 'Ryan', 'Broome')

f1 = Feedback(title="first eddymunsta feedback",
              content="I am eddy and i post  content", username=u1.username)
f2 = Feedback(title="first roman feedback",
              content="I am Roman and this is my content that I like to post", username=u2.username)


# ? send to db
db.session.add_all([u1, u2, ryan, f1, f2])
db.session.commit()
