"""Endpoint definition for authentication."""
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from api import deps
from data import schemas
from services import auth_service
from services.auth_service import get_current_active_user

db = deps.SessionLocal()

router = APIRouter()


class Token(BaseModel):
    """Defines a model for Token."""

    access_token: str
    token_type: str


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Allow the login through a token."""
    return await auth_service.login_for_access_token(form_data)


@router.get("/users/me/", response_model=Optional[schemas.User])
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    """Read the information about logged user."""
    return await auth_service.read_users_me(current_user)


@router.post("/user/", response_model=schemas.UserCreatedWithoutPassword)
async def create_user(raw_user: schemas.UserCreate):
    """Logic to define the login function."""
    return await auth_service.create_user(raw_user)
