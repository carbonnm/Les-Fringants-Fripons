from app import app
import __init__ as init

from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import flash
from flask import jsonify

from models.queries.user_queries import user_can_connect

from flask_login import login_required
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from werkzeug.security import check_password_hash

from models.user import User
from models.forms.login_form import LoginForm

@init.app.login_manager.user_loader
def load_user(user):
    return User.query.get(int(user))

@app.errorhandler(404)
def page_not_found(e):
    """
    Handler of the errors.
    Display 404.html whenever a page is not found
    """
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(e):
    """
    Handler of the errors.
    Display 500.html whenever a server error occures.
    """
    return render_template('errors/500.html'), 500


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login function.
    Redirection to the login page.
    Exceptions :
    ----------------
    User already connected to his account.
    Username does not exist.
    The password is not correct.
    """
    if current_user.is_authenticated :
        flash("You are already connected", "warning")
        return redirect(url_for('homepage'))
    
    form = LoginForm()
    #Verification of the form
    if form.validate_on_submit():
        can_connect, user = user_can_connect(form.email.data, form.password.data)
        #Verification of the user password.
        if user is not None and can_connect:
            login_user(user)
            return redirect(url_for('index'))
        #Password or username might be wrong
        else :
            flash("Incorrect password or username", "warning")
            return redirect(url_for('login'))
    return render_template('login.html',form = form)


@app.route("/logout")
def logout():
    """
    Logout of the user. The user will go back to the home page. 
    Redirection to the main page.
    """
    if current_user.is_authenticated :
        logout_user()
    return redirect(url_for("index"))

@app.route("/profile")
def profile():
    """
    Profile of the user. 
    Redirection to the profile page.
    """
    if current_user.is_authenticated :
        return render_template('profile.html', current_user = current_user)
    return redirect(url_for("login"))


@app.route("/studentListing")
def studentListing():
    students = ["Simon Polet", "Donato Gentile"]
    deletable = True
    return render_template('students_listing.html', students=students, deletable=deletable)