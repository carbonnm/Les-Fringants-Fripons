from __init__ import db
from .hint import Hint

class Question(db.Model):
	"""
	Question class
	--------------
	This class will contain all the information about the questions.
	"""
	__tablename__ = 'question'

	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	question = db.Column(db.String(255), nullable = False)
	vocal = db.Column(db.String(255))
	test = db.Column(db.String(255), db.ForeignKey('test.id', ondelete='CASCADE'), nullable = False)
	answer = db.relationship("Answer", backref="question_answer", cascade='save-update, merge, delete, delete-orphan', lazy='dynamic')
	hint = db.relationship("Hint", backref="question_hint", cascade='save-update, merge, delete, delete-orphan', lazy='dynamic')
