from sqlalchemy.exc import SQLAlchemyError

from ..hint import Hint
from ..question import Question

from __init__ import db


def create_question(question: str, vocal: bytes, test_id: str, hints: [str]):
    """
    Creates a new lesson in the database.

    :param question: The question.
    :param vocal: The vocal recording.
    :param test_id: The id of the test.
    :param hints: The hints of the question.
    """
    question = Question(question=question, vocal=vocal, test=test_id)
    hints = [Hint(hint=hint, question=question.id) for hint in hints]
    try:
        db.session.add(question)
        for hint_entity in hints:
            db.session.add(hint_entity)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise


def get_question_by_id(question_id: int) -> Question:
    """
    Gets a question from the database by its id.

    :param question_id: The id of the lesson.
    :return: The user.
    """
    return Question.query.filter_by(id = question_id).first()


def get_all_questions() -> list[Question]:
    """
    Gets all the lessons from the database.

    :return: A list of lessons.
    """
    return Question.query.all()


def delete_question_by_id(question_id: int):
    """
    Deletes a question from the database by its id.

    :param question_id: The id of the question.
    """
    lesson = get_question_by_id(question_id)
    try:
        db.session.delete(lesson)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise
