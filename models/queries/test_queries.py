from sqlalchemy.exc import SQLAlchemyError

from .. import database_handler
from ..models.test import Test
from ..models.question import Question
from ..queries.lesson_queries import get_lesson_by_id
import question_queries

from app import db


def create_test(test_id: int, lesson_id: int, name: str, questions_list: [Question]):
    """
    Creates a new lesson in the database.

    :param test_id: The id of the test.
    :param lesson_id: The id of the lesson.
    :param name: The name of the test.
    :param questions_list: The list of questions for the test.
    """
    with db.session as session:
        if get_lesson_by_id(lesson_id) is None:
            raise ValueError("This lessons id doesn't exists.")
        if get_test_by_name_and_lesson(name, get_lesson_by_id(lesson_id).name) is not None:
            raise ValueError("A test with the same name already exists.")
        test = Test(id=test_id, name=name, lesson_id=lesson_id, state=False)
        session.begin()
        try:
            session.add(test)
            session.commit()

            for question in questions_list:
                question_queries.create_question(question=question.text, vocal=question.vocal, test_id=question.test_id, hints=question.hints)
        except SQLAlchemyError:
            session.rollback()
            raise


def get_test_by_id(test_id: int) -> Test:
    """
    Gets a test from the database by its id.

    :param test_id: The id of the lesson.
    :return: The user.
    """
    with db.session as session:
        return session.query(Test).filter(Test.id == test_id).first()


def get_test_by_name_and_lesson(test_name: str, lesson_name: str) -> Test:
    """
    Gets a test from the database by its name.

    :param test_name: The name of the lesson.
    :param lesson_name: The name of the lesson.
    :return: The test.
    """
    with db.session as session:
        return session.query(Test).filter(Test.name == test_name and Test.lesson.name == lesson_name).first()


def get_all_tests() -> list[Test]:
    """
   Gets all the tests from the database.

   :return: A list of tests.
   """
    with db.session as session:
        return session.query(Test).all()


def get_all_lesson_tests(lesson_id: id) -> list[Test]:
    """
    Gets all the tests for a specified lesson from the database.

    :return: A list of tests.
    """
    with db.session as session:
        return session.query(Test).filter(Test.lesson == get_lesson_by_id(lesson_id)).all()


def delete_test_by_id(test_id: int):
    """
    Deletes a test from the database by its id.

    :param test_id: The id of the lesson.
    """
    test = get_lesson_by_id(test_id)
    with db.session as session:
        session.begin()
        try:
            session.delete(test)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
