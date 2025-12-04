"""
Authentication module with SHA-256 + salt encryption
"""
import hashlib
import secrets
from database.connection import execute_query


def generate_salt():
    """Generate a random 16-byte salt"""
    return secrets.token_hex(16)


def hash_password(password, salt):
    """
    Hash password using SHA-256 with salt
    
    Args:
        password: Plain text password
        salt: Random salt string
    
    Returns:
        Hashed password string
    """
    salted_password = password + salt
    return hashlib.sha256(salted_password.encode()).hexdigest()


def verify_password(password, stored_hash, salt):
    """
    Verify password against stored hash
    
    Args:
        password: Plain text password to verify
        stored_hash: Stored password hash
        salt: Salt used during hashing
    
    Returns:
        True if password matches, False otherwise
    """
    computed_hash = hash_password(password, salt)
    return computed_hash == stored_hash


def create_user(username, email, password):
    """
    Create a new user account
    
    Args:
        username: User's chosen username
        email: User's email address
        password: Plain text password
    
    Returns:
        user_id if successful, None otherwise
    """
    # Check if username or email already exists
    existing = execute_query(
        "SELECT user_id FROM users WHERE username = %s OR email = %s",
        (username, email),
        fetch_one=True
    )
    
    if existing:
        return None
    
    # Generate salt and hash password
    salt = generate_salt()
    password_hash = hash_password(password, salt)
    
    # Insert new user
    user_id = execute_query(
        """INSERT INTO users (username, email, password_hash, salt) 
           VALUES (%s, %s, %s, %s)""",
        (username, email, password_hash, salt)
    )
    
    return user_id


def authenticate_user(username, password):
    """
    Authenticate a user by username and password
    
    Args:
        username: User's username
        password: Plain text password
    
    Returns:
        User dict if authenticated, None otherwise
    """
    user = execute_query(
        """SELECT user_id, username, email, password_hash, salt 
           FROM users WHERE username = %s""",
        (username,),
        fetch_one=True
    )
    
    if user and verify_password(password, user['password_hash'], user['salt']):
        return {
            'user_id': user['user_id'],
            'username': user['username'],
            'email': user['email']
        }
    
    return None


def get_user_by_id(user_id):
    """
    Get user information by ID
    
    Args:
        user_id: User's ID
    
    Returns:
        User dict or None
    """
    return execute_query(
        "SELECT user_id, username, email, created_at FROM users WHERE user_id = %s",
        (user_id,),
        fetch_one=True
    )
