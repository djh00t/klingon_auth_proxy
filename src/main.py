"""
This module defines a FastAPI app that requires authentication using JWT tokens.
It defines a root endpoint that returns a message for authenticated users.
"""
import os
import logging
from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from .login import app as login_app
from .secrets import SECRET_KEY

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# FILEPATH: src/main.py

# Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uvicorn.error")

# Create FastAPI app
app = FastAPI()

app.mount("/login", login_app)

# Security
security = HTTPBearer()

# Import SECRET_KEY from secrets module
from .secrets import SECRET_KEY
APP_PORT = os.environ.get("APP_PORT", 9111)

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT, log_level="debug")
