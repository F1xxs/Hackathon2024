import sqlite3
import hashlib
import logging
import uuid
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",
    filemode="a"
)


DB = 'database.db'


def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def sign_up(username, password):
    """Signs up a user by storing their username and hashed password."""
    hashed_password = hash_password(password)

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    query = "INSERT INTO users (username, password) VALUES (?, ?)"
    cursor.execute(query, (username, hashed_password))

    conn.commit()
    conn.close()

    logging.info("User registered successfully!")


def create_session(user_id, duration_days=7):
    """Creates a session for a given user."""
    session_id = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=duration_days)

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    query = '''
    INSERT INTO sessions (user_id, session_id, expires_at) VALUES (?, ?, ?);
    '''
    cursor.execute(query, (user_id, session_id, expires_at))
    conn.commit()
    conn.close()
    logging.info(f"Session created for user {
                 user_id} with session ID: {session_id}")
    return session_id


def login(username, password):
    """Validates user login by checking username and hashed password."""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    query = "SELECT password FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    conn.close()

    if result:
        stored_hashed_password = result[0]
        if stored_hashed_password == hash_password(password):
            logging.info(f"User '{username}' logged in successfully.")
            return True
        else:
            logging.warning(f"Failed login attempt for user: '{
                            username}' (incorrect password).")
            return False
    else:
        logging.warning(
            f"Failed login attempt for non-existent user: '{username}'.")

        return False
