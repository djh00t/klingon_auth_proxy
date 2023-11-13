"""
This module defines a FastAPI app that requires authentication using JWT tokens.
It defines a root endpoint that returns a message for authenticated users.
"""
import os
from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from .login import app as login_app
import secrets

# FILEPATH: src/main.py

# Create FastAPI app
app = FastAPI()

app.mount("/login", login_app)

# Security
security = HTTPBearer()

# Constants
HTACCESS_FILE = os.environ.get("HTACCESS_FILE", "../secrets")
APP_PORT = os.environ.get("APP_PORT", 9111)

# Generate secret.key if it doesn't exist
def get_or_create_secret_key(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        secret_key = secrets.token_urlsafe(32)
        with open(file_path, "w") as file:
            file.write(secret_key)
        return secret_key

# Generate SECRET_KEY if it doesn't exist otherwise read the file.
SECRET_KEY = get_or_create_secret_key("secret.key")

# Check credentials
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Returns the payload of a valid JWT token from the Authorization header.

    Args:
        credentials (HTTPAuthorizationCredentials): The Authorization header credentials.

    Raises:
        HTTPException: If the token is invalid or the Authorization header is missing.

    Returns:
        The payload of the JWT token.
    """
    if credentials:
        try:
            payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
            return payload
        except JWTError:
            raise HTTPException(status_code=403, detail="Invalid token")
    else:
        raise HTTPException(status_code=401, detail="Authorization header missing")

app = FastAPI()

@app.get("/")
async def root():
    return RedirectResponse(url="/login")

