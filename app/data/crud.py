"""Definition of Create, Read, Update and Delete operations for database operations."""
from datetime import datetime
from datetime import timezone
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import joinedload

from api import deps
from data import models
from data import schemas

db = deps.SessionLocal()


def get_user_by_username(username: str):
    """Get an user."""
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(email: str):
    """Get an user."""
    return db.query(models.User).filter(models.User.email == email).first()


def activate_user_by_email(email: str):
    """Activate an user by email."""
    session = (
        db.query(models.User)
        .filter(models.User.email == email)
        .update({models.User.enable: True})
    )
    db.commit()
    return session


def create_user(request: schemas.UserCreatedWithPassword):
    """Create an user."""
    user_group: models.Group = (
        db.query(models.Group).filter(models.Group.name == "user").first()
    )

    db_user = models.User(**request.dict())
    user_group.users.append(db_user)
    db.commit()

    return get_user_by_email(request.email)


def get_permissions() -> List[models.Permission]:
    """Get permissions."""
    return db.query(models.Permission).all()


def get_permissions_by_username(username: str) -> List[models.Permission]:
    """Get permissions by username."""
    user_permissions = db.query(models.Permission).filter(
        models.Permission.users.any(username=username)
    )

    user_groups = db.query(models.Group.id).filter(
        models.Group.users.any(username=username)
    )

    group_permissions = db.query(models.Permission).filter(
        models.Permission.groups.any(models.Group.id.in_(user_groups))
    )

    return user_permissions.union_all(group_permissions)
