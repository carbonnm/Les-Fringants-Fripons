from sqlalchemy import Integer, ForeignKey, String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .test import Test
from .base_table import BaseTable


class Question(BaseTable):
	__tablename__ = 'question'

	id: Mapped[Integer] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
	question: Mapped[String] = mapped_column(String, nullable=False)
	vocal: Mapped[LargeBinary] = mapped_column(LargeBinary)
	test: Mapped[Test] = mapped_column(String, ForeignKey('test.id', ondelete='CASCADE'), nullable=False)
	answer = relationship("Answer", backref="question_answer", cascade='save-update, merge, delete, delete-orphan', lazy='dynamic')
	hint = relationship("Hint", backref="question_hint", cascade='save-update, merge, delete, delete-orphan', lazy='dynamic')