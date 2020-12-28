"""Definition of Schemas for the database integration."""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel
from pydantic import EmailStr


class UserBase(BaseModel):
    """Schema for Base User Definition."""

    username: str
    full_name: str
    email: EmailStr


class UserCreate(UserBase):
    """Schema for User Creation Definition."""

    password: str


class UserCreatedWithPassword(UserBase):
    """Schema for User Creation with Password Definition."""

    hashed_password: str


class UserCreatedWithoutPassword(UserBase):
    """Schema for User Creation without Password Definition."""

    pass

    class Config:
        """Additional Configuration for the User Created Without Password Definition."""

        orm_mode = True


class User(UserBase):
    """Schema for User Definition."""

    id: int
    enable: bool = True
    hashed_password: str

    class Config:
        """Additional Configuration for the User Definition."""

        orm_mode = True


class OsmTags(BaseModel):
    """Schema for OSM tags."""

    amenity: Optional[str] = None
    name: Optional[str] = None

    class Config:
        """Additional Configuration for the OsmTags Definition."""

        orm_mode = True


class OsmElements(BaseModel):
    """Schema for OSM elements."""

    type: Optional[str] = None
    id: Optional[int] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    tags: Optional[OsmTags] = None

    class Config:
        """Additional Configuration for the OsmElements Definition."""

        orm_mode = True


class Osm(BaseModel):
    """Schema for OSM responses."""

    elements: List[OsmElements] = []

    class Config:
        """Additional Configuration for the Osm Definition."""

        orm_mode = True


class QueryLog(BaseModel):
    """ Schema for the Querylog Definition."""

    query_string: str
    created_at: datetime

    class Config:
        """Additional Configuration for the QueryLog Definition."""

        orm_mode = True
