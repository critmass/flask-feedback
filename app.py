from crypt import methods
import os
import requests as requests_api
from sqlalchemy.exc import IntegrityError

from flask import Flask, render_template, request, flash, redirect, session
from models import User, Feedback, db, connect_db
from db_access import localDatabase
from form import RegistrationForm, LoginForm, FeedbackForm

CURRENT_USER_KEY="curr_user"

app = Flask(__name__)

connect_db(app)
db.create_all()

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get(localDatabase)
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")


# helpers
#######################################################################


def do_login(user):
    """Log in user."""

    session[CURRENT_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURRENT_USER_KEY in session:
        del session[CURRENT_USER_KEY]


def secretPage():
    if "user_id" not in session:
        flash("you are not logged in")
        return redirect("/login")


# Routes
#####################################################################

@app.route("/")
def home():
    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('registration.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('registration.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/user/")

        flash("Invalid credentials.", 'danger')

    return render_template('log_in.html', form=form)

@app.route('/logout', methods=["POST"])
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You are logged out, thanks for visiting!", 'info')

    return redirect("/login")


@app.route('/users/<username>')
def getUser(username):
    user = User.query.first_or_404(username)
    if not user:
        return redirect("/err404")
    feedback = Feedback.query.get(username)

    return render_template(
        "userInfo.html",
        feedback=feedback,
        username=username
    )

@app.route('/users/<username>/delete', methods=["POST"])
def deleteUser(username):
    user = User.query.get(username)

    db.session.delete(user)
    db.session.commit()

@app.route('/users/<username>/feedback/add', methods=['POST', 'GET'])
def addFeedback(username):

    form = FeedbackForm()

    if form.valid_on_submit():
        feedback = Feedback(
            username=username,
            title=form.title.data,
            content=form.content.data
        )
        db.session.add(feedback)
        db.session.commit()

        flash("Feedback added successfully", 'success')

    return render_template('feedback.html', form=form)

@app.route('/feedback/<feedbackId>/update', methods=['POST', 'GET'])
def updateFeedback(feedbackId):

    feedback = Feedback.query.first_or_404(feedbackId)

    form = FeedbackForm(obj=feedback)

    if form.valid_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()

        flash("Feedback updated successfully", 'success')

    return render_template('feedback.html', form=form)

@app.route('/feedback/<feedbackId>/delete', methods=['POST'])
def deleteFeedback(feedbackId):
    feedback = Feedback.query.first_or_404(feedbackId)
    db.session.delete(feedback)
    db.session.commit()

@app.route('/err404')
def error404():
    return render_template("error_404.html")






