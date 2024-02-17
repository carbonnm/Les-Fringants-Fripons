from sqlalchemy.exc import SQLAlchemyError

from .. import database_handler
from ..models.hint import Hint
from ..models.question import Question

DATABASE_HANDLER = database_handler.get_instance_database()


def create_question(question: str, vocal: bytes, test_id: str, hints: [str]):
    """
    Creates a new lesson in the database.

    :param question: The question.
    :param vocal: The vocal recording.
    :param test_id: The id of the test.
    :param hints: The hints of the question.
    """
    with DATABASE_HANDLER.get_session() as session:
        question = Question(question=question, vocal=vocal, test=test_id)
        hints = [Hint(hint=hint, question=question.id) for hint in hints]
        session.begin()
        try:
            session.add(question)
            for hint_entity in hints:
                session.add(hint_entity)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise


def get_question_by_id(question_id: int) -> Question:
    """
    Gets a question from the database by its id.

    :param question_id: The id of the lesson.
    :return: The user.
    """
    with DATABASE_HANDLER.get_session() as session:
        return session.query(Question).filter(Question.id == question_id).first()


def get_all_questions() -> list[Question]:
    """
    Gets all the lessons from the database.

    :return: A list of lessons.
    """
    with DATABASE_HANDLER.get_session() as session:
        return session.query(Question).all()


def delete_question_by_id(question_id: int):
    """
    Deletes a question from the database by its id.

    :param question_id: The id of the question.
    """
    lesson = get_question_by_id(question_id)
    with DATABASE_HANDLER.get_session() as session:
        session.begin()
        try:
            session.delete(lesson)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
