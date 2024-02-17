from __init__ import db
from .question import Question


class Test(db.Model):
	"""
	Test class
	--------------
	This class will contain all the information about the tests.
	"""
	__tablename__ = 'test'

	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	name = db.Column(db.String(255), nullable = False)
	code = db.Column(db.String(255), nullable = False)
	state = db.Column(db.Boolean, nullable = False)
	lesson = db.Column(db.Integer, db.ForeignKey('lesson.id', ondelete='CASCADE'), nullable = False)
	question = db.relationship("Question", backref = "test_question", cascade = 'save-update, merge, delete, delete-orphan', lazy = 'dynamic')
