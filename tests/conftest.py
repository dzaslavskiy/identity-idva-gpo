"""fixtures"""
import sys
from typing import Generator

import pytest
from fastapi.testclient import TestClient

import db
from db import SessionLocal

# pylint: disable=wrong-import-position
sys.modules["gpo.database"] = db
from gpo.main import app
from gpo.models import Letter


@pytest.fixture
def generate_data():
    """test fixture"""

    def get_letter() -> Letter:
        """get a letter object"""
        return Letter(
            id=5,
            name="Name",
            address="Address",
            address2="Address 2",
            city="City",
            state="State",
            zip="Zip",
            code="Code",
            date="Date",
            expiry="Date",
            app="App",
            url="Url",
        )

    return get_letter


@pytest.fixture(scope="session")
def session() -> Generator:
    """session"""
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    """api test client"""
    with TestClient(app) as test_client:
        yield test_client
