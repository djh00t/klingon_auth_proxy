import os
import secrets

# Constants
HTACCESS_FILE = os.environ.get("HTACCESS_FILE", "secrets")

import hashlib

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
                    if hasher.hexdigest() == hashed_password:
                        return algorithm
    except FileNotFoundError:
        pass
    return None

HASHING_ALGORITHM = get_hashing_algorithm(HTACCESS_FILE)



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
