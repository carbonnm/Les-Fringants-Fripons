from sqlalchemy.exc import SQLAlchemyError

from ..lesson import Lesson
from .user_queries import get_user_by_id

from __init__ import db


def create_lesson(teacher_id: int, name: str):
	"""
	Creates a new lesson in the database.

	:param teacher_id: The id of the professor.
	:param name: The name of the lesson.

	"""
	if get_lesson_by_name(name) is not None:
		raise ValueError("A lesson with the same name already exists.")
	if get_user_by_id(teacher_id) is None:
		raise ValueError("This professor id doesn't exists.")
	lesson = Lesson(name=name, teacher=teacher_id)

	try:
		db.session.add(lesson)
		db.session.commit()
	except SQLAlchemyError:
		db.session.rollback()
		raise


def get_lesson_by_id(lesson_id: int) -> Lesson:
	"""
	Gets a lesson from the database by its id.

	:param lesson_id: The id of the lesson.
	:return: The user.
	"""
	return Lesson.query.filter_by(id = lesson_id).first()


def get_lesson_by_name(lesson_name: str) -> Lesson:
	"""
	Gets a user from the database by its name.

	:param lesson_name: The name of the lesson.
	:return: The user.
	"""
	return Lesson.query.filter_by(name = lesson_name).first()


def get_all_lessons() -> list[Lesson]:
	"""
	Gets all the lessons from the database.

	:return: A list of lessons.
	"""
	return Lesson.query.all()


def get_all_lessons_by_professor(teacher_id: int) -> list[Lesson]:
	"""
	Gets all the lessons from the database by the teacher id.

	:param teacher_id: The id of the teacher.
	:return: A list of lessons.
	"""
	return Lesson.query.filter_by(teacher = teacher_id).all()


def delete_lesson_by_id(lesson_id: int):
	"""
	Deletes a lesson from the database by its id.

	:param lesson_id: The id of the lesson.
	"""
	lesson = get_lesson_by_id(lesson_id)
	try:
		db.session.delete(lesson)
		db.session.commit()
	except SQLAlchemyError:
		db.session.rollback()
		raise
