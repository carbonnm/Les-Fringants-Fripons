from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_table import BaseTable


class User(BaseTable):
	__tablename__ = 'user'

	id: Mapped[Integer] = mapped_column(Integer, primary_key=True, nullable=False)
	firstname: Mapped[String] = mapped_column(String(50), nullable=False)
	name: Mapped[String] = mapped_column(String(50), nullable=False)
	role: Mapped[String] = mapped_column(String(50), nullable=False)
	email: Mapped[String] = mapped_column(String(50), nullable=False, unique=True)
	password: Mapped[String] = mapped_column(String(50), nullable=False)
	lesson = relationship("Lesson", backref="user_lesson", cascade='save-update, merge, delete, delete-orphan', lazy='dynamic')
	answer = relationship("Answer", backref="user_answer", cascade='save-update, merge, delete, delete-orphan', lazy='dynamic')