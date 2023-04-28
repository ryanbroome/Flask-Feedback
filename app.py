from flask import Flask, jsonify, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Feedback
from forms import UserForm, RegisterForm, FeedbackForm


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_users_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "super-sized-secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

# ?  GET redirect to /register
@app.route("/")
def show_base_page():
    return render_template('base.html')


# ? GET , POST /register when submitted register/create user
@app.route("/register", methods=["GET", "POST"])
def process_register_form():
    # * create form instance using WTForm
    form = RegisterForm()

    # * validate form on submit
    if form.validate_on_submit():
        username = form.username.data.lower()
        password = form.password.data
        email = form.email.data.lower()
        first_name = form.first_name.data
        last_name = form.last_name.data

        # *with valid form data create an instance of User model use the class method .register to hash PWD with form data
        new_user = User.register(username=username, password=password, email=email,
                                 first_name=first_name, last_name=last_name)

        # * add the new username to the current session
        session['username'] = new_user.username.lower()

        # * commit new user to the db
        db.session.add(new_user)
        db.session.commit()

        # * flash a success message that has been added
        flash(f"User {new_user.username} has been added")

        # * redirect to the home page at successful completion
        # ! This is where you will REDIRECT upon successful registration of a new_user, maybe a user_detail or info page
        return redirect(f"/users/{new_user.username}")

    else:

        # * if unsuccessful or no data in form redirect to the form template page
        return render_template("register_form.html", form=form)

# ?GET /details user details
@app.route('/details')
def show_details():
    if "username" not in session:
        flash("Please login first")
        return redirect("/login")
    return render_template("details.html")

# ? GET /login Show a form that when submitted will login a user. This form should accept a username and password
@app.route("/login")
def show_login_form():
    form = UserForm()
    return render_template("login_form.html", form=form)


# ? POST / login Process the login form, ensuring the user is authenticated and going to /secret if so
@app.route("/login", methods=["POST"])
def process_login_form():
    #  create instance of UserForm
    form = UserForm()

    # validate form data on submit
    if form.validate_on_submit():
        username = form.username.data.lower()
        password = form.password.data

        # use class method to authenticate user, compare db pwd to user input pwd
        user = User.authenticate(username, password)

        # if validated redirect to details, passing user object to template
        if user:

            # welcome message
            flash(f"Welcome Back! {user.username}")

            # set user to the session
            session["username"] = user.username.lower()

            #  to  details page
            return redirect(f"/users/{user.username}")
        else:
            # throw form field error
            form.username.errors = ["Invalid username/password"]
    #  not validated?  login / register?
    return render_template("login_form.html", form=form)

# ? GET /feedback Return the text "you made it!" (don't worry we'll get rid of this soon)
@app.route('/feedback', methods=["GET", "POST"])
def show_feedback():
    """when user logged into session show feedback form and feedback for user"""

    # * check session for logged in user, flash, redirect if no user in session
    if 'username' not in session:
        flash("Please login or Register first")
        return redirect("/login")

    # *if user logged in, create instance of Feedback Form
    else:
        form = FeedbackForm()

        # *query all feedback
        all_feedback = Feedback.query.all()
    # * validate form on submit

    # *capture needed variables from form.variable.data can do .lower() .upper()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        username = session['username']

        # *create new feedback instance using these variables from form.variable.data
        new_feedback = Feedback(
            title=title,
            content=content,
            username=username)

        # *commit new feedback to the database
        db.session.add(new_feedback)
        db.session.commit()
        # *flash success message
        flash('Feedback created')
        # *redirect back to feedback as a GET request
        return redirect('/feedback')

    # *render feedback template, pass in form and all_feedback
    return render_template("feedback.html", form=form, all_feedback=all_feedback)

# ? POST / logout the user
@app.route('/logout', methods=["GET", "POST"])
def logout_user():
    session.pop("username")
    flash("Successfully logged you out, Goodbye!")
    return redirect('/')


# ? GET /users/<username>
@app.route("/users/<username>")
def show_user_details(username):
    """Show user details for username"""

    if username not in session["username"]:
        flash("Please login first!")
        return redirect("/login")

    else:

        user = User.query.filter_by(username=username).first()
        user_feedback = user.feedback

        return render_template("details.html", user=user, user_feedback=user_feedback)
