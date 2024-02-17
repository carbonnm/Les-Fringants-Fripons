from sqlalchemy.exc import SQLAlchemyError

from ..test import Test
from ..question import Question
from .lesson_queries import get_lesson_by_id
from .question_queries import create_question

from __init__ import db


def create_test(lesson_id: int, name: str, questions_list: [Question]):
    """
    Creates a new lesson in the database.

    :param lesson_id: The id of the lesson.
    :param name: The name of the test.
    :param questions_list: The list of questions for the test.
    """
    if get_lesson_by_id(lesson_id) is None:
        raise ValueError("This lessons id doesn't exists.")
    if get_test_by_name_and_lesson(name, get_lesson_by_id(lesson_id).name) is not None:
        raise ValueError("A test with the same name already exists.")
    test = Test(name=name, lesson=lesson_id, code=random_code(), state=False)
    print(test.name, test.code, test.state, test.lesson, test.id)
    try:
        db.session.add(test)
        db.session.commit()
        for question in questions_list:
            create_question(question=question.text, vocal=question.vocal, test_id=question.test_id, hints=question.hints)
    except SQLAlchemyError:
        db.session.rollback()
        raise


def get_test_code_by_id(test_id: int) -> str:
    """
    Gets the code of a test from the database by its id.

    :param test_id: The id of the test.
    :return: The code of the test.
    """
    return Test.query.filter_by(id=test_id).first().code


def get_test_by_id(test_id: int) -> Test:
    """
    Gets a test from the database by its id.

    :param test_id: The id of the test.
    :return: The user.
    """
    return Test.query.filter_by(id=test_id).first()


def get_test_by_name_and_lesson(test_name: str, lesson_name: str) -> Test | None:
    """
    Gets a test from the database by its name.

    :param test_name: The name of the lesson.
    :param lesson_name: The name of the lesson.
    :return: The test or None if not found.
    """
    tests = Test.query.filter_by(name=test_name).all()
    results = list(filter(lambda test: test.lesson.name == lesson_name, tests))
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
    return Test.query.filter_by(lesson=get_lesson_by_id(lesson_id)).all()


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


def random_code():
    """
    Generates a random code for a test.

    :return: The random code.
    """
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))