import os
import secrets
import hashlib
import logging

# Create a logger
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

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
                for algorithm in hashlib.algorithms_guaranteed:
                    hasher = hashlib.new(algorithm)
                    hasher.update(username.encode())
                    try:
                        if hasher.hexdigest() == hashed_password:
                            logger.info(f"Hashing algorithm for {file_path} detected: {algorithm}")
                            return algorithm
                    except TypeError:
                        # Some algorithms like 'shake_128' and 'shake_256' require a length argument
                        for length in range(1, 65):  # Try lengths from 1 to 64
                            if hasher.hexdigest(length) == hashed_password:
                                logger.info(f"Hashing algorithm for {file_path} detected: {algorithm}")
                                return algorithm
    except FileNotFoundError:
        pass
    return 'sha256'

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

# Generate SECRET_KEY if it doesn't exist otherwise read the file.
SECRET_KEY = get_or_create_secret_key("secret.key")
