"""Definition for authentication services."""
from datetime import datetime
from datetime import timedelta
from typing import Dict
from typing import List
from typing import Optional

from fastapi import Depends
from fastapi import HTTPException
from fastapi import Security
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import SecurityScopes
from jose import jwt
from jose import JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from pydantic import ValidationError

import config
from data import crud
from data import schemas

SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


class TokenData(BaseModel):
    """Defines a model for TokenData."""

    username: str
    scopes: List[str] = []


def __get_permissions() -> Optional[Dict[str, str]]:
    permissions = crud.get_permissions()
    return {permission.code: permission.description for permission in permissions}


scopes = {"admin": "Super admin scope", "user": "Normal user scope"}
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scopes=scopes)


def __verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    """Get the password hash from a string."""
    return pwd_context.hash(password)


def __get_user(username: str) -> Optional[schemas.User]:
    return crud.get_user_by_username(username)


def __authenticate_user(username: str, password: str):
    user = __get_user(username)
    if not user or not user.enable:
        return False
    if not __verify_password(password, user.hashed_password):
        return False
    return user


def __get_user_permissions(username: str):
    return crud.get_permissions_by_username(username)


async def __send_confirmation_email(email_: str):
    # TODO: send confirmation mail
    pass


def __create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
):
    """Get current user with security scopes."""
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = __get_user(username=token_data.username)

    if user is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes and "admin" not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: schemas.User = Security(get_current_user, scopes=["user"])
):
    """Get the current user information."""
    if not current_user.enable:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Allow the login through a token."""
    user = __authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    permissions = __get_user_permissions(user.username)

    scopes = [
        permission.code
        for permission in permissions
        if permission.code in form_data.scopes
    ]

    access_token = __create_access_token(
        data={"sub": user.username, "scopes": scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    """Read the information about logged user."""
    return current_user


async def validation_token(token: str):
    """Validate the token."""

    # TODO: must be the token validation done. Must set user.enable = True
    return True


async def create_user(raw_user: schemas.UserCreate):
    """Logic to define the login function."""
    hashed_password = get_password_hash(raw_user.password)
    user = schemas.UserCreatedWithPassword(
        **raw_user.dict(), hashed_password=hashed_password
    )

    user_exists = crud.get_user_by_email(user.email)

    if user_exists:
        raise HTTPException(status_code=401, detail="User already exists")

    user_exists = crud.get_user_by_username(user.username)

    if user_exists:
        raise HTTPException(status_code=401, detail="User already exists")

    user = crud.create_user(user)

    if not user:
        raise HTTPException(status_code=500, detail="User can't be created")

    # await __send_confirmation_email(user.email)

    return user


async def resend_email_confirmation(email_: str):
    """Logic to resend the email confirmation."""
    user = crud.get_user_by_email(email_)

    if user:
        # await __send_confirmation_email(user.email)
        return True

    return False
