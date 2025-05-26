"""Authentication module for FastAPI using Basic Auth."""

import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from config import settings

security = HTTPBasic()


def basic_auth(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    """
    Dependency for Basic Auth authentication.

    Validates the provided username and password against the settings.

    :params credentials: HTTPBasicCredentials
    :raises HTTPException: If authentication fails.
    :return: Username if authentication is successful.
    """
    is_authenticated = all((
        secrets.compare_digest(credentials.username, settings.USERNAME),
        secrets.compare_digest(credentials.password, settings.PASSWORD),
    ))

    if not is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
