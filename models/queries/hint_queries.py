from sqlalchemy.exc import SQLAlchemyError

from .. import database_handler
from ..models.hint import Hint
from .question_queries import get_question_by_id
from app import db


def create_hint(hint: str, question_id: int):
    """
    Creates a new lesson in the database.

    :param hint: The hint.
    :param question_id: The question's id of the hint.

    """
    with db.session as session:
        if get_question_by_id(question_id) is None:
            raise ValueError("This question id doesn't exists.")
        hint = Hint(hint=hint, question=question_id)

        session.begin()
        try:
            session.add(hint)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise


def get_hint_by_id(hint_id: int) -> Hint:
    """
    Gets a hint from the database by its id.

    :param hint_id: The id of the lesson.
    :return: The user.
    """
    with db.session as session:
        return session.query(Hint).filter(Hint.id == hint_id).first()


def get_all_hints() -> list[Hint]:
    """
    Gets all the lessons from the database.

    :return: A list of lessons.
    """
    with db.session as session:
        return session.query(Hint).all()


def delete_hint_by_id(hint_id: int):
    """
    Deletes a hint from the database by its id.

    :param hint_id: The id of the hint.
    """
    lesson = get_hint_by_id(hint_id)
    with db.session as session:
        session.begin()
        try:
            session.delete(lesson)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
