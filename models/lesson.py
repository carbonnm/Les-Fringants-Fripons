from __init__ import db
from .test import Test

class Lesson(db.Model):
	"""
	Lesson class
	--------------
	This class will contain all the information about the lessons.
	"""
	__tablename__ = 'lesson'

	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	name = db.Column(db.String(255), nullable = False)
	student = db.Column(db.String(255), db.ForeignKey('user.id', ondelete='CASCADE'))
	test = db.relationship("Test", backref="lesson_test", cascade='save-update, merge, delete, delete-orphan', lazy='dynamic')