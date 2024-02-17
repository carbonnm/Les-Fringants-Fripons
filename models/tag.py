from __init__ import db


class Tag(db.Model):
	"""
	Tag class
	--------------
	This class will contain all the information about the tags.
	"""
	__tablename__ = 'tag'

	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	name = db.Column(db.String(255), nullable = False)
	user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable = False)
	