from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import User
from .base_table import BaseTable


class Lesson(BaseTable):
	__tablename__ = 'lesson'

	id: Mapped[Integer] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
	name: Mapped[String] = mapped_column(String, nullable=False)
	professor: Mapped[User] = mapped_column(String, ForeignKey('user.id', ondelete='CASCADE'))
	student: Mapped[User] = mapped_column(String, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
	test = relationship("Test", backref="lesson_test", cascade='save-update, merge, delete, delete-orphan', lazy='dynamic')
