"""Definition of Models for integration with endpoints."""
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from data.database import Base

group_permissions_table = Table(
    "group_permissions",
    Base.metadata,
    Column("group_id", Integer, ForeignKey("groups.id")),
    Column("permission_id", Integer, ForeignKey("permissions.id")),
)

user_permissions_table = Table(
    "user_permissions",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("permission_id", Integer, ForeignKey("permissions.id")),
)

user_groups_table = Table(
    "user_groups",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("group_id", Integer, ForeignKey("groups.id")),
)


class Permission(Base):
    """Model for the Permission Definition."""

    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    description = Column(String, nullable=False)

    users = relationship(
        "User", secondary=user_permissions_table, back_populates="permissions"
    )
    groups = relationship(
        "Group", secondary=group_permissions_table, back_populates="permissions"
    )


class Group(Base):
    """Model for the Group Definition."""

    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    permissions = relationship(
        "Permission", secondary=group_permissions_table, back_populates="groups"
    )

    users = relationship("User", secondary=user_groups_table, back_populates="groups")


class User(Base):
    """Model for the User Definition."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    # TODO: must be enabled after mail verification
    enable = Column(Boolean, default=True, nullable=False)

    permissions = relationship(
        "Permission", secondary=user_permissions_table, back_populates="users"
    )

    groups = relationship("Group", secondary=user_groups_table, back_populates="users")
