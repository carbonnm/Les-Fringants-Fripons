import bcrypt
from sqlalchemy.exc import SQLAlchemyError

from .. import database_handler
from ..models.lesson import Lesson

DATABASE_HANDLER = database_handler.get_instance_database()


def create_lesson(lesson_id: int, name: str):
	"""
	Creates a new lesson in the database.

	:param lesson_id: The name of the lesson.
	:param name: The name of the lesson.

	"""
	with DATABASE_HANDLER.get_session() as session:
		if get_lesson_by_name(name) is not None:
			raise ValueError("A lesson with the same name already exists.")


		lesson = Lesson(id=lesson_id, name=name)#TODO
		session.begin()
		try:
			session.add(lesson)
			session.commit()
		except SQLAlchemyError:
			session.rollback()
			raise


def get_lesson_by_id(lesson_id: int) -> Lesson:
	"""
	Gets a lesson from the database by its id.

	:param lesson_id: The id of the lesson.
	:return: The user.
	"""
	with DATABASE_HANDLER.get_session() as session:
		return session.query(Lesson).filter(Lesson.id == id).first()


def get_lesson_by_name(lesson_name: str) -> Lesson:
	"""
	Gets a user from the database by its email.

	:param lesson_name: The name of the lesson.
	:return: The user.
	"""
	with DATABASE_HANDLER.get_session() as session:
		return session.query(Lesson).filter(Lesson.name == lesson_name).first()


def get_all_lesson() -> list[Lesson]:
	"""
	Gets all the lessons from the database.

	:return: A list of lessons.
	"""
	with DATABASE_HANDLER.get_session() as session:
		return session.query(Lesson).all()


def delete_lesson_by_id(lesson_id: int):
	"""
	Deletes a lesson from the database by its id.

	:param lesson_id: The id of the lesson.
	"""
	lesson = get_lesson_by_id(lesson_id)
	with DATABASE_HANDLER.get_session() as session:
		session.begin()
		try:
			session.delete(lesson)
			session.commit()
		except SQLAlchemyError:
			session.rollback()
			raise
