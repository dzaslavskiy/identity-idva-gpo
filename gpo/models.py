"""
Models for GPO
"""
import sqlalchemy as sqla
from sqlalchemy.ext import declarative

# pylint: disable=too-few-public-methods

Base = declarative.declarative_base()


class Letter(Base):
    """
    DB model for Letter
    """

    __tablename__ = "letters"

    id = sqla.Column(sqla.Integer, primary_key=True, index=True)
    name = sqla.Column(sqla.String)
    address = sqla.Column(sqla.String)
    address2 = sqla.Column(sqla.String)
    city = sqla.Column(sqla.String)
    state = sqla.Column(sqla.String)
    zip = sqla.Column(sqla.String)
    code = sqla.Column(sqla.String)
    date = sqla.Column(sqla.String)
    expiry = sqla.Column(sqla.String)
    app = sqla.Column(sqla.String)
    url = sqla.Column(sqla.String)

    def as_list(self, index: str) -> list:
        """
        Convert Letter to a list of fields

        index is a formatted line number
        """
        return [
            index,
            self.name,
            self.address,
            self.address2,
            self.city,
            self.state,
            self.zip,
            self.code,
            self.date,
            self.expiry,
            self.app,
            self.url,
        ]
