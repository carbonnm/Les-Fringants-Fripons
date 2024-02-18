import os
from models.objects.question import Question
import models.queries.user_queries as user_queries
import models.queries.tag_queries as tag_queries

from __init__ import app, db
from flask import flash, redirect, render_template, url_for, request, send_from_directory
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.utils import secure_filename

from models.queries.user_queries import get_user_by_email
from models.queries.lesson_queries import create_lesson, get_lesson_by_name
from models.queries.test_queries import get_all_tests, create_test, does_code_exist, get_test_by_code, get_test_by_id
from models.queries.question_queries import get_all_answers, get_all_question_hints, get_questions_by_test_id, create_question
from models.forms.login_form import LoginForm
from flask import redirect, render_template, flash

db.create_all()
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if user_queries.get_user_by_email("admin@admin.com") is None:
	user_queries.create_user("admin", "admin", "admin@admin.com", "admin", "admin")
	user_queries.create_user("Wim", "Vanhoof", "wim.vanhoof@unamur.be", "motdepasse123", "teacher")
	user_queries.create_user("Donato", "Gentile", "donato.gentile@student.unamur.be", "motdepasse123", "student")
	user_queries.create_user("Mehdi", "Bouzid", "mehdi.bouzid@gmail.com", "motdepasse123", "student")
	user_queries.create_user("Pierre", "Lambert", "pierre.lambert@hotmail.com", "motdepasse123", "student")
	
	tag_queries.create_tag("Visual", user_queries.get_user_by_email("donato.gentile@student.unamur.be").id)
	tag_queries.create_tag("Auditory", user_queries.get_user_by_email("mehdi.bouzid@gmail.com").id)
	#tag_queries.create_tag("Matteo Minded", user_queries.get_user_by_email("pierre.lambert@hotmail.com").id)
	tag_queries.create_tag("Need extra help", user_queries.get_user_by_email("pierre.lambert@hotmail.com").id)

	create_lesson(teacher_id=get_user_by_email("wim.vanhoof@unamur.be").id, name="Probabilités et Statistiques")
	create_lesson(teacher_id=get_user_by_email("wim.vanhoof@unamur.be").id, name="Algorithmique et programmation")
	create_lesson(teacher_id=get_user_by_email("wim.vanhoof@unamur.be").id, name="Introduction à l'informatique")

	create_test(lesson_id=get_lesson_by_name("Probabilités et Statistiques").id, name="Examen Bac 2 janvier 2023", questions_list=[])
	create_test(lesson_id=get_lesson_by_name("Probabilités et Statistiques").id, name="Examen Bac 2 juin 2024", questions_list=[])
	create_test(lesson_id=get_lesson_by_name("Introduction à l'informatique").id, name="Examen Bac 1 janvier 2023", questions_list=[])
	create_test(lesson_id=get_lesson_by_name("Introduction à l'informatique").id, name="Examen mystère", 
			 questions_list=[Question(text="""
### Problème : Forces et Tensions dans un Système de Poulies

Un bloc de masse m1 = 5 kg est suspendu par une corde qui passe sur une poulie fixe, puis descend verticalement pour être attaché à un second bloc de masse m2 = 3 kg qui repose sur une surface horizontale sans frottement. Un troisième bloc de masse m3 = 4 kg est suspendu par une autre corde attachée au second bloc.

1. Calculez la tension dans la corde reliant le premier bloc au second.
2. Déterminez la tension dans la corde reliant le second bloc au troisième.
3. Quelle est l'accélération du système entier ?
4. Si la masse m2 est retirée, comment cela affectera-t-il l'accélération du système ?
""", vocal=None, hints=[]), 
					Question(text="", vocal=None, hints=[problem_description = """
### Problème : Forces et Tensions dans un Système de Poulies

Un bloc de masse **m1 = 5 kg** est suspendu par une corde qui passe sur une poulie fixe, puis descend verticalement pour être attaché à un second bloc de masse **m2 = 3 kg** qui repose sur une surface horizontale sans frottement. Un troisième bloc de masse **m3 = 4 kg** est suspendu par une autre corde attachée au second bloc.

1. Calculez la **tension** dans la corde reliant le premier bloc au second.
2. Déterminez la **tension** dans la corde reliant le second bloc au troisième.
3. Quelle est l'**accélération** du système entier ?
4. Si la masse **m2** est retirée, comment cela affectera-t-il l'**accélération** du système ?

**Indice :** Pour résoudre ce problème, utilisez les principes de la **conservation de l'énergie** et les lois de **Newton** pour les mouvements rectilignes et circulaires.
"""
]),
					Question(text= "", vocal= None, hints= [])])


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
	if current_user.role == "student":
		return redirect(url_for("enter_code"))
	return redirect(url_for("teacherEvaluations"))


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


@app.route("/createTest")
@login_required
def createTest():
    return render_template('create_test.html')


@app.route("/modifyTest/<id>", methods = ['GET'])
def modifyTest(id):
	test = get_test_by_id(id)
	questions = get_questions_by_test_id(id)
	hints_query = get_all_question_hints
	return render_template('modify_test.html', test=test, questions=questions, hints_query=hints_query)


@app.route("/correctEvaluation")
@login_required
def correctEvaluation():
    questions = ["Question 1", "Question 2", "Question3"]
    return render_template('correct_evaluation.html', questions = questions)


@app.route("/correctQuestion")
@login_required
def correctQuestion():
    return render_template("correct_question.html")

@app.route("/upload", methods = ['POST'])
@login_required
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
@login_required
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route("/record")
@login_required
def record():
    return render_template('record.html')


@app.route("/enter_code")
@login_required
def enter_code():
	return render_template('enter_code.html')


@app.route("/test/<code>")
@login_required
def join(code):
	if does_code_exist(code):
		# Todo: redirect to the test page
		test = get_test_by_code(code)
		questions = get_questions_by_test_id(test.id)
		hints_query = get_all_question_hints
		return render_template('pass_evaluation.html', test=test, questions=questions, hints_query=hints_query)
	else:
		# flash('The code is not correct. Please try again.', 'error')
		return redirect('/enter_code')


@app.route("/api/addtest", methods=["POST"])
@login_required
def add_test():
	data = request.json
	title = data['title']
	questions = data['questions']
	lesson_id = 1 # We don't have the lesson list implemented for the demo
	questions_list = [Question(question["question"], "", [question["hint"]]) for question in questions]
	create_test(lesson_id, title, questions_list)
	return "Test added", 200
