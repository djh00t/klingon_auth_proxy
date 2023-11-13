import os
import secrets
import hashlib
import logging

# Create a logger
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

# Constants
HTACCESS_FILE = os.environ.get("HTACCESS_FILE", "secrets")

logger.info(f"HTACCESS_FILE is: {HTACCESS_FILE}")

# Confirm the type of hashing used in HTACCESS_FILE
def get_hashing_algorithm(file_path):
    """
    Determines the type of hashing used in the given htaccess file.

    Args:
        file_path (str): The path to the htaccess file.

    Returns:
        str: The name of the hashing algorithm if a match is found, None otherwise.
    """
    try:
        with open(file_path, 'r') as file:
            line = file.readline().strip()
            if line:
                username, hashed_password = line.split(':', 1)
                if hashed_password.startswith("$apr1$"):
                    logger.info(f"Hashing algorithm for {file_path} detected: apr1_crypt")
                    return "apr1_crypt"
    except FileNotFoundError:
        pass
    return 'bcrypt'

HASHING_ALGORITHM = get_hashing_algorithm(HTACCESS_FILE)

logger.info(f"HASHING_ALGORITHM is: {HASHING_ALGORITHM}")


# Generate secret.key if it doesn't exist
def get_or_create_secret_key(file_path):
    """
    Reads the secret key from the given file path, or creates a new one if the file does not exist.

    Args:
        file_path (str): The path to the file containing the secret key.

    Returns:
        str: The secret key read from the file or newly generated if the file did not exist.
    """
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        secret_key = secrets.token_urlsafe(32)
        with open(file_path, "w") as file:
            file.write(secret_key)
        return secret_key

def list_users(file_path):
    """
    Reads the usernames from the given htaccess file.

    Args:
        file_path (str): The path to the htaccess file.
    """
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip():
                    username, _ = line.strip().split(':', 1)
                    logger.debug(f"User found: {username}")
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")

# Generate SECRET_KEY if it doesn't exist otherwise read the file.
SECRET_KEY = get_or_create_secret_key("secret.key")

# List users in HTACCESS_FILE
list_users(HTACCESS_FILE)
