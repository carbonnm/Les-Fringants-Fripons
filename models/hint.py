from __init__ import db


class Hint(db.Model):
	__tablename__ = 'hint'

	id = db.Column(db.Integer, primary_key=True, nullable=False)
	hint = db.Column(db.String(50), nullable=False)
	question = db.Column(db.String, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False)