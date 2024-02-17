from __init__ import app, db
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

import models.queries.user_queries as user_queries
from models.queries.user_queries import get_user_by_email
from models.queries.lesson_queries import create_lesson, get_all_lessons, get_lesson_by_name
import models.queries.tag_queries as tag_queries
from models.queries.test_queries import get_all_tests, create_test

from models.queries.lesson_queries import get_all_lessons_by_professor
from models.forms.login_form import LoginForm
from models.user import User

db.create_all()

if user_queries.get_user_by_email("admin@admin.com") is None:
	user_queries.create_user("admin", "admin", "admin@admin.com", "admin", "admin")
	user_queries.create_user("Wim", "Vanhoof", "wim.vanhoof@unamur.be", "motdepasse123", "teacher")
	user_queries.create_user("Donato", "Gentile", "donato.gentile@student.unamur.be", "motdepasse123", "student")
	user_queries.create_user("Mehdi", "Bouzid", "mehdi.bouzid@gmail.com", "motdepasse123", "student")
	user_queries.create_user("Pierre", "Lambert", "pierre.lambert@hotmail.com", "motdepasse123", "student")
	
	tag_queries.create_tag("Visual", user_queries.get_user_by_email("donato.gentile@student.unamur.be").id)
	tag_queries.create_tag("Auditory", user_queries.get_user_by_email("mehdi.bouzid@gmail.com").id)
	tag_queries.create_tag("Matteo Minded", user_queries.get_user_by_email("pierre.lambert@hotmail.com").id)
	tag_queries.create_tag("Need extra help", user_queries.get_user_by_email("pierre.lambert@hotmail.com").id)

	create_lesson(teacher_id=get_user_by_email("wim.vanhoof@unamur.be").id, name="Probabilités et Statistiques")
	create_lesson(teacher_id=get_user_by_email("wim.vanhoof@unamur.be").id, name="Algorithmique et programmation")
	create_lesson(teacher_id=get_user_by_email("wim.vanhoof@unamur.be").id, name="Introduction à l'informatique")

	create_test(lesson_id=get_lesson_by_name("Probabilités et Statistiques").id, name="Examen Bac 2 janvier 2023", questions_list=[])
	create_test(lesson_id=get_lesson_by_name("Probabilités et Statistiques").id, name="Examen Bac 2 juin 2024", questions_list=[])
	create_test(lesson_id=get_lesson_by_name("Introduction à l'informatique").id, name="Examen Bac 1 janvier 2023", questions_list=[])


@app.login_manager.user_loader
def load_user(user):
	return user_queries.get_user_by_id(int(user))

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
@login_required
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
@login_required
def logout():
	"""
	Logout of the user. The user will go back to the home page. 
	Redirection to the main page.
	"""
	if current_user.is_authenticated :
		logout_user()
	return redirect(url_for("index"))

@app.route("/profile")
@login_required
def profile():
	"""
	Profile of the user. 
	Redirection to the profile page.
	"""
	if current_user.is_authenticated :
		return render_template('profile.html', current_user = current_user)
	return redirect(url_for("login"))

@app.route("/studentListing")
@login_required
def studentListing():
	students = user_queries.get_all_students()
	return render_template('students_listing.html', students=students)

@app.route("/teacherEvaluations")
@login_required
def teacherEvaluations():
	if current_user.role == "student":
		return redirect(url_for("index"))
	evaluations = get_all_tests()
	return render_template('teacher_evaluations.html', evaluations=evaluations)