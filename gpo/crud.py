"""
CRUD operations for gpo µservice
"""
import sqlalchemy
from sqlalchemy import orm

from . import models, schemas


def count_letters(session: orm.Session) -> int:
    """
    count letters
    """
    return session.scalar(sqlalchemy.select(sqlalchemy.func.count(models.Letter.id)))


def get_letters(
    session: orm.Session, skip: int = 0, limit: int = 1000
) -> list[models.Letter]:
    """
    get letters
    """
    statement = sqlalchemy.select(models.Letter).offset(skip).limit(limit)
    return session.execute(statement).scalars().all()


def get_letters_for_update(
    session: orm.Session, skip: int = 0, limit: int = 1000
) -> list[models.Letter]:
    """
    get letters with lock
    """
    statement = (
        sqlalchemy.select(models.Letter).with_for_update().offset(skip).limit(limit)
    )
    return session.execute(statement).scalars().all()


def delete_letters(session: orm.Session, letters: list[models.Letter]):
    """
    delete list of letters by instance
    """

    for letter in letters:
        session.delete(letter)

    session.commit()


def create_letter(session: orm.Session, letter: schemas.LetterCreate) -> models.Letter:
    """
    create letter
    """
    db_item = models.Letter(**letter.dict())
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item
