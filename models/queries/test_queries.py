from sqlalchemy.exc import SQLAlchemyError

from test import Test
from question import Question
from lesson_queries import get_lesson_by_id
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
    if get_lesson_by_id(lesson_id) is None:
        raise ValueError("This lessons id doesn't exists.")
    if get_test_by_name_and_lesson(name, get_lesson_by_id(lesson_id).name) is not None:
        raise ValueError("A test with the same name already exists.")
    test = Test(id=test_id, name=name, lesson_id=lesson_id, state=False)
    try:
        db.session.add(test)
        db.session.commit()
        for question in questions_list:
            question_queries.create_question(question=question.text, vocal=question.vocal, test_id=question.test_id, hints=question.hints)
    except SQLAlchemyError:
        db.session.rollback()
        raise


def get_test_by_id(test_id: int) -> Test:
    """
    Gets a test from the database by its id.

    :param test_id: The id of the test.
    :return: The user.
    """
    return Test.filter_by(id=test_id).first()


def get_test_by_name_and_lesson(test_name: str, lesson_name: str) -> Test | None:
    """
    Gets a test from the database by its name.

    :param test_name: The name of the lesson.
    :param lesson_name: The name of the lesson.
    :return: The test or None if not found.
    """
    tests = Test.filter_by(name=test_name).all()
    results = filter(lambda test: test.lesson.name == lesson_name, tests)
    return results[0] if len(results) > 0 else None


def get_all_tests() -> list[Test]:
    """
   Gets all the tests from the database.

   :return: A list of tests.
   """
    return Test.query.all()


def get_all_lesson_tests(lesson_id: id) -> list[Test]:
    """
    Gets all the tests for a specified lesson from the database.

    :return: A list of tests.
    """
    return Test.query.filter(lesson=get_lesson_by_id(lesson_id)).all()


def delete_test_by_id(test_id: int):
    """
    Deletes a test from the database by its id.

    :param test_id: The id of the lesson.
    """
    test = get_lesson_by_id(test_id)
    try:
        db.session.delete(test)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise
