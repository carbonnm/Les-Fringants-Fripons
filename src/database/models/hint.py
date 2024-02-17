from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .question import Question
from .base_table import BaseTable


class Hint(BaseTable):
	__tablename__ = 'hint'

	id: Mapped[Integer] = mapped_column(Integer, primary_key=True, nullable=False)
	type: Mapped[String] = mapped_column(String(50), nullable=False)
	hint: Mapped[String] = mapped_column(String(50), nullable=False)
	question: Mapped[Question] = mapped_column(String, ForeignKey('question.id', ondelete='CASCADE'), nullable=False)
