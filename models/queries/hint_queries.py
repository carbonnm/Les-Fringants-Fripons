from sqlalchemy.exc import SQLAlchemyError

from hint import Hint
from question_queries import get_question_by_id
from app import db


def create_hint(hint: str, question_id: int):
    """
    Creates a new lesson in the database.

    :param hint: The hint.
    :param question_id: The question's id of the hint.

    """
    if get_question_by_id(question_id) is None:
        raise ValueError("This question id doesn't exists.")
    hint = Hint(hint=hint, question=question_id)
    try:
        db.session.add(hint)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise


def get_hint_by_id(hint_id: int) -> Hint:
    """
    Gets a hint from the database by its id.

    :param hint_id: The id of the lesson.
    :return: The user.
    """
    return db.select(Hint).filter_by(id = hint_id).first()


def get_all_hints() -> list[Hint]:
    """
    Gets all the lessons from the database.

    :return: A list of lessons.
    """
    return Hint.query.all()


def delete_hint_by_id(hint_id: int):
    """
    Deletes a hint from the database by its id.

    :param hint_id: The id of the hint.
    """
    lesson = get_hint_by_id(hint_id)
    try:
        db.session.delete(lesson)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise
