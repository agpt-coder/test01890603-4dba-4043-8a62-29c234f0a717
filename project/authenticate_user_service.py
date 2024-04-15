from datetime import datetime, timedelta

import prisma
import prisma.models
from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


class AuthenticateUserResponse(BaseModel):
    """
    This model represents the response data after a user has been authenticated successfully. It primarily includes an access token for the user.
    """

    access_token: str
    token_type: str
    expires_in: int


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def authenticate_user(email: str, password: str) -> AuthenticateUserResponse:
    """
    Authenticates a user and provides an access token.

    Args:
    email (str): User's email address used for authentication.
    password (str): User's password used for authentication.

    Returns:
    AuthenticateUserResponse: This model represents the response data after a user has been authenticated successfully. It primarily includes an access token for the user.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(password, user.hashedPassword):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return AuthenticateUserResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a password against a hashed version.

    Args:
        plain_password (str): Plain text password.
        hashed_password (str): Hashed password for verification.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): Data to include in the JWT payload.
        expires_delta (timedelta): Amount of time for the token to be valid.

    Returns:
        str: A JWT encoded access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
