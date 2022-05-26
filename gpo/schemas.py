"""
REST api models for gpo µservice
"""
import pydantic

# pylint: disable=too-few-public-methods


class LetterBase(pydantic.BaseModel):
    """
    base letter model
    """

    name: str
    address: str
    address2: str
    city: str
    state: str
    zip: str
    code: str
    date: str
    expiry: str
    app: str
    url: str


class LetterCreate(LetterBase):
    """
    create letter model
    """


class Letter(LetterBase):
    """
    read letter model
    """

    id: int

    class Config:
        """
        config for model
        """

        orm_mode = True


class Count(pydantic.BaseModel):
    """count of letters"""

    count: int
