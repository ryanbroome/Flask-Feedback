# from secrets_1 import SECRET
from flask import Flask, jsonify, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Feedback
from forms import UserForm, RegisterForm, FeedbackForm
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_users_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# new os import
app.config["SECRET_KEY"] = os.environ.get('SECRET_key', 'secret1')

app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

# ?  GET redirect to /register
@app.route("/")
def show_base_page():
    return render_template('base.html')

# ? GET, POST /register when submitted register/create user
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
        flash(f"User {new_user.username} has been added", "success")

        # * redirect to the home page at successful completion
        # ! This is where you will REDIRECT upon successful registration of a new_user, maybe a user_detail or info page
        return redirect(f"/users/{new_user.username}")

    else:

        # * if unsuccessful or no data in form redirect to the form template page
        return render_template("register_form.html", form=form)

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
        username = form.username.data
        password = form.password.data

        # use class method to authenticate user, compare db pwd to user input pwd
        user = User.authenticate(username, password)

        # if validated redirect to details, passing user object to template
        # if user.username == session["username"]:
        if user:

            # welcome message
            flash(f"Welcome Back! {user.username}", "primary")

            # set user to the session
            session["username"] = user.username

            #  to  details page
            return redirect(f"/users/{user.username}")
    else:
            # throw form field error
        form.username.errors = ["Invalid username/password"]
    #  not validated?  login / register?
    return render_template("login_form.html", form=form)

# ? GET/POST feedback
@app.route('/feedback', methods=["GET", "POST"])
def show_feedback():
    """when user logged into session show feedback form and feedback for user"""

    # * check session for logged in user, flash, redirect if no user in session
    if 'username' not in session:
        flash("Please login or Register first", "danger")
        return redirect("/login")

    # *if user logged in, create instance of Feedback Form
    else:
        form = FeedbackForm()

        # *query all feedback
        all_feedback = Feedback.query.all()

    # * validate form on submit
    # *capture needed variables from form.variable.data .lower()
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
        flash('Feedback created', "success")

        # *redirect back to feedback as a GET request
        return redirect('/feedback')

    # *render feedback template, pass in form and all_feedback
    return render_template("feedback.html", form=form, all_feedback=all_feedback)

# ? POST / logout the user
@app.route('/logout', methods=["GET", "POST"])
def logout_user():
    session.pop("username")
    flash("Successfully logged you out, Goodbye!", "success")
    return redirect('/')

# ? GET /users/<username>
@app.route("/users/<username>")
def show_user_details(username):
    """Show user details for single user"""
    if username not in session["username"]:
        flash("Please login first!", "danger")
        return redirect("/login")

    else:
        user = User.query.filter_by(username=username).first()
        if user.feedback:
            user_feedback = user.feedback
            return render_template("details.html", user=user, user_feedback=user_feedback)
        else:
            return render_template("details.html", user=user)

# ? POST /users/<username>/delete
@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """delete user details for username given from database"""
    user = User.query.get_or_404(username)
    if user.username == session["username"]:
        all_feedback = user.feedback
        for f in all_feedback:
            db.session.delete(f)
            db.session.commit()
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        flash("User and all user feedback have been deleted", "info")
        return redirect("/")

    # ! LEFT OFF WITH ADDING DELETE ROUTES FOR A USER AND A FEEDBACK

# ? POST /feedback/<id>/delete
@app.route("/feedback/<int:id>/delete", methods=["POST"])
def delete_feedback(id):
    """delete single feedback instance"""

    # * get feedback from db
    feedback = Feedback.query.get_or_404(id)

    # * check if feedback.username not in session then they can't delete and need to login
    if feedback.username not in session["username"]:
        return redirect('/login')

    # * check if username of feedback equals logged in user
    if feedback.username == session["username"]:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback has been deleted", "danger")
        return redirect(f"/users/{session['username']}")
        # return redirect(f"/users/{feedback.username}")

# ? GET | POST  "/users/<username>/feedback/add"
@app.route("/users/<username>/feedback/add", methods=["POST", "GET"])
def show_feedback_form(username):
    """render details template and show feedback form"""
    # * check session for logged in user, flash, redirect if no user in session
    if 'username' not in session:
        flash("Please login or Register first", "danger")
        return redirect("/login")

    # *if user logged in, create instance of Feedback Form
    else:
        form = FeedbackForm()

        # * validate form on submit
        # *capture needed variables from form.variable.data
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            username = session['username']

            # *create new feedback instance using these variables from form.variable.data
            new_feedback = Feedback(
                title=title,
                content=content,
                username=username)

            # *commit/update new feedback to the database
            db.session.add(new_feedback)
            db.session.commit()

            # *flash success message
            flash('Feedback created', "success")

            # *redirect back to feedback as a GET request
            return redirect(f'/users/{username}')

        # *render feedback template, pass in form and all_feedback
        return render_template("feedback_form.html", form=form)

# # ? GET | feedback/update
@app.route("/feedback/<feedback_id>/update", methods=["GET"])
def show_update_form(feedback_id):
    """show update form to update a feedback"""
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)

    # * check if feedback.username not in session then they can't delete and need to login
    if feedback.username not in session["username"]:
        flash(f"Only the author can update a feedback", "info")
        return redirect('/login')

    return render_template("update_feedback_form.html", form=form, feedback=feedback)

#  ? POST | /feedback/<feedback_id>/update
@app.route("/feedback/<feedback_id>/update", methods=["POST"])
def process_update_form(feedback_id):
    """Process a form to update feedback, only by the user that wrote feedback"""
    # * get feedback from db
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm()

    # * check if feedback.username not in session then they can't update
    if feedback.username not in session["username"]:
        # * need to login
        flash(f"Only the author can update a feedback", "info")
        return redirect('/login')

     # * check if username of feedback equals logged in user
    if feedback.username == session["username"]:

        # * validate form on submit
        # *capture needed variables from form.variable.data
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            # // username = session['username']

            # *update feedback instance using these variables from form.variable.data
            feedback.title = title
            feedback.content = content

            # *commit new feedback to the database
            db.session.commit()

            # * flash and redirect to user details page
            flash("Feedback has been updated", "info")
            return redirect(f"/users/{session['username']}")
