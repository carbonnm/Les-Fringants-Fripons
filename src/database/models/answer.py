from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .question import Question
from .base_table import BaseTable


class Answer(BaseTable):
	__tablename__ = 'answer'

	id: Mapped[Integer] = mapped_column(Integer, primary_key=True, nullable=False)
	answer: Mapped[String] = mapped_column(String(200), nullable=False)
	question: Mapped[Question] = mapped_column(String, ForeignKey('question.id', ondelete='CASCADE'), nullable=False)
