"""Definition of Schemas for the database integration."""
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
