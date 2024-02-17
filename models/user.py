from flask_login import UserMixin
from sqlalchemy import ForeignKey
from .lesson import Lesson
from .answer import Answer
from .tag import Tag
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
	tag = db.relationship('Tag', backref="user_tag", cascade='save-update, merge, delete, delete-orphan', lazy='dynamic')
