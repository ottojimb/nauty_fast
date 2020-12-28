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


class __ModelStatus(BaseModel):
    status: bool


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Allow the login through a token."""
    return await auth_service.login_for_access_token(form_data)


@router.get("/users/me/", response_model=Optional[schemas.User])
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    """Read the information about logged user."""
    return await auth_service.read_users_me(current_user)


@router.get("/token_confirmation/{token}", response_model=__ModelStatus)
async def validation_token(token: str):
    """Validate the token."""
    status_ = await auth_service.validation_token(token)
    return {"status": status_}


@router.post("/user/", response_model=schemas.UserCreatedWithoutPassword)
async def create_user(raw_user: schemas.UserCreate):
    """Logic to define the login function."""
    return await auth_service.create_user(raw_user)


@router.post("/resend_email_confirmation/", response_model=__ModelStatus)
async def resend_email_confirmation(email: str):
    """Logic to resend the email confirmation."""
    status_ = await auth_service.resend_email_confirmation(email)
    return {"status": status_}
