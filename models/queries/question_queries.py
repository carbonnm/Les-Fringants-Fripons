from sqlalchemy.exc import SQLAlchemyError

from models.answer import Answer

from ..hint import Hint
from ..question import Question

from __init__ import db


def create_question(question: str, vocal: bytes, test_id: int, hints: [str]): # type: ignore
    """
    Creates a new lesson in the database.

    :param question: The question.
    :param vocal: The vocal recording.
    :param test_id: The id of the test.
    :param hints: The hints of the question.
    """
    question = Question(question=question, vocal=vocal, test=test_id)
    try:
        db.session.add(question)
        db.session.commit()
        hints = [Hint(hint=hint, question=question.id) for hint in hints]
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


def get_questions_by_test_id(test_id: int) -> list[Question]:
    """
    Gets all the questions from the database by the test id.

    :param test_id: The id of the test.
    :return: A list of questions.
    """
    return Question.query.filter_by(test=test_id).all()


def get_all_question_hints(question_id: int) -> list[Hint]:
    """
    Gets all the hints from the database by the question id.

    :param question_id: The id of the question.
    :return: A list of hints.
    """
    return Hint.query.filter_by(question=question_id).all()


def get_all_answers(question_id: int) -> list[Hint]:
    """
    Gets all the answers from the database by the question id.

    :param question_id: The id of the question.
    :return: A list of answers.
    """
    return Answer.query.filter_by(question=question_id).all()


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
