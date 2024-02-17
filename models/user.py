from flask_login import UserMixin
from .lesson import Lesson
from .answer import Answer
from __init__ import db


class User(UserMixin, db.Model) :
	"""
	User class
	--------------
	This class will contain all the information about the users who have an account.
	"""
	#Initialisation
	__tablename__ = 'user'

	#DB
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	firstname = db.Column(db.String(255), nullable = False)
	name = db.Column(db.String(255), nullable = False)
	role = db.Column(db.String(255), nullable = False)
	email = db.Column(db.String(255), nullable = False, unique = True)
	password = db.Column(db.String(255), nullable = False)
	lesson = db.relationship('Lesson', backref="user_lesson", cascade='save-update, merge, delete, delete-orphan', lazy='dynamic')
	answer = db.relationship('Answer', backref="user_answer", cascade='save-update, merge, delete, delete-orphan', lazy='dynamic')
	
	# def getname(self) :
	# 	"""
	# 	Getter of the username.
	# 	Return : 
	# 	----------
	# 	Username
	# 	"""
	# 	return self.name

	# def setPassword(self, password) :
	# 	"""
	# 	Setter of the password in the database.
	# 	We use for that the function generate_password_hash so that the password is cripted in the database.
	# 	"""
	# 	self.password = generate_password_hash(password)
	# 	db.session.commit()
	
	# def checkPassword(self, password) :
	# 	"""
	# 	Check if the password do correspond.
	# 	Return :
	# 	----------
	# 	True if the passwords do correspond, False otherwise.
	# 	"""
	# 	return check_password_hash(self.password, password)

	# def __repr__(self) :
	# 	"""
	# 	How users will be represented.
	# 	Return :
	# 	----------
	# 	Representation of a user.
	# 	"""
	# 	return "<User id : %d, username : %s, lastName : %s, firstName : %s, email : %s>" % (self.id, self.username, self.lastName, self.firstName, self.email)
	
