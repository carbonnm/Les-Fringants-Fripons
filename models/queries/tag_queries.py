from sqlalchemy.exc import SQLAlchemyError

from models.tag import Tag

from __init__ import db

def create_tag(name: str, user_id: int):
    """
    Creates a new tag in the database.

    :param name: The tag name.
    """
    tag = Tag(name=name, user=user_id)
    try:
        db.session.add(tag)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise ValueError("An error occurred while creating the tag.")


def get_tag_by_id(tag_id) -> Tag:
    """
    Gets a tag from the database by its id.

    :param tag_id: The id of the tag.
    :return: The tag.
    """
    return Tag.query.filter_by(id=tag_id).first()


def get_tag_by_name(name) -> Tag:
    """
    Gets a tag from the database by its name.

    :param name: The name of the tag.
    :return: The tag.
    """
    return Tag.query.filter_by(name=name).first()


def get_all_tags() -> list[Tag]:
    """
    Gets all the tags from the database.

    :return: A list of tags.
    """
    return Tag.query.all()


def delete_tag_by_name(name):
    """
    Deletes a tag from the database by its name.

    :param name: The name of the tag.
    """
    tag = get_tag_by_name(name)
    if tag is not None:
        db.session.delete(tag)
        db.session.commit()
    else:
        raise ValueError("The tag doesn't exist.")
    

def delete_tag_by_id(tag_id):
    """
    Deletes a tag from the database by its id.

    :param tag_id: The id of the tag.
    """
    tag = get_tag_by_id(tag_id)
    if tag is not None:
        db.session.delete(tag)
        db.session.commit()
    else:
        raise ValueError("The tag doesn't exist.")