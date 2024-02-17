import bcrypt
from sqlalchemy.exc import SQLAlchemyError

from models.user import User

from __init__ import db


def create_user(firstname: str, name: str, email: str, password: str, role: str = "student"):
	"""
	Creates a new user in the database.

	:param firstname: The firstname of the user.
	:param name: The name of the user.
	:param email: The email of the user.
	:param password: The password of the user.
	:param role: The role of the user.
	"""
	if get_user_by_email(email) is not None:
		raise ValueError("A user with the same email already exists.")

	salt = bcrypt.gensalt()
	password = bcrypt.hashpw(password.encode(), salt)
	user = User(firstname=firstname, name=name, role=role, email=email, password=password)
	try:
		db.session.add(user)
		db.session.commit()
	except SQLAlchemyError:
		db.session.rollback()
		raise


def get_user_by_id(user_id: int) -> User:
	"""
	Gets a user from the database by its id.

	:param user_id: The id of the user.
	:return: The user.
	"""
	return User.query.get(user_id)
	
	
def get_user_by_email(user_email: str) -> User:	
	"""
	Gets a user from the database by its email.

	:param user_email: The email of the user.
	:return: The user.
	"""
	return User.query.filter_by(email=user_email).first()


def get_all_users() -> list[User]:
	"""
	Gets all the users from the database.

	:return: A list of users.
	"""
	return User.query.all()


def get_all_students() -> list[User]:
	"""
	Gets all the students from the database.

	:return: A list of students.
	"""
	return User.query.filter_by(role="student").all()


def delete_user_by_id(user_id: int):
	"""
	Deletes a user from the database by its id.

	:param user_id: The id of the user.
	"""
	user = get_user_by_id(user_id)
	try:
		db.session.delete(user)
		db.session.commit()
	except SQLAlchemyError:
		db.session.rollback()
		raise


def get_user_tags_by_id(user_id: int) -> list[str]:
	"""
	Gets all the tags of a user from the database by its id.

	:param user_id: The id of the user.
	:return: A list of tags.
	"""
	user = get_user_by_id(user_id)
	return user.tag


def user_can_connect(user_email: str, password: str) -> (bool, User):
	"""
	Checks if a user is in the database and if the password is correct.

	:param user_email: The email of the user.
	:param password: The password of the user.
	:return: A boolean indicating whether the user can connect with the given password and the user object itself.
	"""
	user = get_user_by_email(user_email)
	can_connect = user is not None and bcrypt.checkpw(password.encode(), user.password)
	return can_connect, user if can_connect else None
