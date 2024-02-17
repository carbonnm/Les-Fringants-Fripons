from sqlalchemy import String, Integer, ForeignKey
from  __init__ import db


class Answer(db.Model):
	__tablename__ = 'answer'

	id = db.Column(Integer, primary_key=True, nullable=False)
	answer = db.Column(String(200), nullable=False)
	question = db.Column(String, ForeignKey('question.id', ondelete='CASCADE'), nullable=False)
	user = db.Column(String, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)