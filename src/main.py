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
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

# FILEPATH: src/main.py

# Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uvicorn.error")

import os

# Create FastAPI app
app = FastAPI()

# Check if templates directory exists and create it if it doesn't
if not os.path.exists('templates'):
    os.makedirs('templates')

# Check if login.html exists and create it if it doesn't
login_html_path = os.path.join('templates', 'login.html')
if not os.path.exists(login_html_path):
    with open(login_html_path, 'w') as f:
        f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f7f7f7; text-align: center; padding: 50px; }
        form { background-color: white; padding: 40px; border-radius: 10px; display: inline-block; }
        input { margin: 10px 0; padding: 10px; width: 200px; border-radius: 5px; border: 1px solid #ddd; }
        button { padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <form action="/login" method="post">
        <h2>Login</h2>
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
""")

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
