"""Module to define dependencies for the v1 api."""
from typing import Generator

from data.database import SessionLocal


def get_db() -> Generator:
    """Database generator to close any connection on close."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
