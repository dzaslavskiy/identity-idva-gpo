"""crud test"""
from sqlalchemy.orm import Session

from gpo import crud


def test_get_item(session: Session) -> None:
    """test get"""
    crud.get_letters(session)


def test_get_item_for_update(session: Session) -> None:
    """test get for update"""
    crud.get_letters_for_update(session)
