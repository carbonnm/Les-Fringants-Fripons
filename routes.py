from __init__ import app, db
from flask import flash, redirect, render_template, url_for, request, send_from_directory
from flask_login import current_user, login_user, logout_user
import os
from werkzeug.utils import secure_filename

import models.queries.user_queries as user_queries

from models.forms.login_form import LoginForm
from models.user import User

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if user_queries.get_user_by_email("admin@admin.com") is None:
    user_queries.create_user("admin", "admin", "admin@admin.com", "admin", "admin")

@app.login_manager.user_loader
def load_user(user):
    db.create_all()
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
        return redirect('/')
    
    form = LoginForm()
    #Verification of the form
    if form.validate_on_submit():
        can_connect, user = user_queries.user_can_connect(form.email.data, form.password.data)
        #Verification of the user password.
        if user is not None and can_connect:
            login_user(user)
            return redirect(url_for('index'))
        #Password or username might be wrong
        else :
            flash("Incorrect password or username", "warning")
            return redirect(url_for('login'))
    return render_template('./forms/login.html',form = form)


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
    return render_template('students_listing.html', students=students)

@app.route("/teacherEvaluations")
def teacherEvaluations():
    evaluations = ["Math", "Physics", "Psycho"]
    return render_template('teacher_evaluations.html', evaluations=evaluations)


@app.route("/createTest")
def createTest():
    return render_template('create_test.html')


@app.route("/modifyTest")
def modifyTest():
    return render_template('modify_test.html')


@app.route("/correctEvaluation")
def correctEvaluation():
    questions = ["Question 1", "Question 2", "Question3"]
    return render_template('correct_evaluation.html', questions = questions)


@app.route("/correctQuestion")
def correctQuestion():
    return render_template("correct_question.html")

@app.route("/upload", methods = ['POST'])
def upload():
    if 'audio' not in request.files:
        return 'Aucun fichier audio trouvé', 400

    audio_file = request.files['audio']

    if audio_file.filename == '':
        return 'Aucun fichier audio sélectionné', 400

    if audio_file:
        # Assurez-vous que le nom de fichier est sécurisé
        filename = secure_filename(audio_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Enregistrez le fichier audio sur le serveur
        audio_file.save(filepath)

        return 'Fichier audio enregistré avec succès', 200
    

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route("/record")
def record():
    return render_template('record.html')