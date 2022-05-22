"""
Models for GPO
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# pylint: disable=too-few-public-methods

Base = declarative_base()


class Letter(Base):
    """
    DB model for Letter
    """

    __tablename__ = "letters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    address2 = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    code = Column(String)
    date = Column(String)
    expiry = Column(String)
    app = Column(String)
    url = Column(String)

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
