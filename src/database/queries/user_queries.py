import bcrypt
from sqlalchemy.exc import SQLAlchemyError

from .. import database_handler
from ..models.user import User

DATABASE_HANDLER = database_handler.get_instance_database()


def create_user(firstname: str, name: str, email: str, password: str, role: str = "student"):
	"""
	Creates a new user in the database.

	:param firstname: The firstname of the user.
	:param name: The name of the user.
	:param email: The email of the user.
	:param password: The password of the user.
	:param role: The role of the user.
	"""
	with DATABASE_HANDLER.get_session() as session:
		if get_user_by_email(email) is not None:
			raise ValueError("A user with the same email already exists.")

		salt = bcrypt.gensalt()
		password = bcrypt.hashpw(password.encode(), salt)
		user = User(firstname=firstname, name=name, role=role, email=email, password=password)
		session.begin()
		try:
			session.add(user)
			session.commit()
		except SQLAlchemyError:
			session.rollback()
			raise


def get_user_by_id(user_id: int) -> User:
	"""
	Gets a user from the database by its id.

	:param user_id: The id of the user.
	:return: The user.
	"""
	with DATABASE_HANDLER.get_session() as session:
		return session.query(User).filter(User.id == user_id).first()
	
	
def get_user_by_email(user_email: str) -> User:	
	"""
	Gets a user from the database by its email.

	:param user_email: The email of the user.
	:return: The user.
	"""
	with DATABASE_HANDLER.get_session() as session:
		return session.query(User).filter(User.email == user_email).first()	


def get_all_users() -> list[User]:
	"""
	Gets all the users from the database.

	:return: A list of users.
	"""
	with DATABASE_HANDLER.get_session() as session:
		return session.query(User).all()


def delete_user_by_id(user_id: int):
	"""
	Deletes a user from the database by its id.

	:param user_id: The id of the user.
	"""
	user = get_user_by_id(user_id)
	with DATABASE_HANDLER.get_session() as session:
		session.begin()
		try:
			session.delete(user)
			session.commit()
		except SQLAlchemyError:
			session.rollback()
			raise


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
