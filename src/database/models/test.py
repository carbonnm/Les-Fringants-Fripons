from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .lesson import Lesson
from .base_table import BaseTable


class Test(BaseTable):
	__tablename__ = 'test'

	id: Mapped[Integer] = mapped_column(Integer, primary_key=True, nullable=False)
	name: Mapped[String] = mapped_column(String(50), nullable=False)
	state: Mapped[Boolean] = mapped_column(Boolean, nullable=False)
	lesson: Mapped[Lesson] = mapped_column(String, ForeignKey('lesson.id', ondelete='CASCADE'), nullable=False)
	question = relationship("Question", backref="test_question", cascade='save-update, merge, delete, delete-orphan', lazy='dynamic')
