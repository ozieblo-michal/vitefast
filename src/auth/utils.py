from passlib.context import CryptContext

# Security setup for password hashing.
# Bcrypt is chosen as the hashing algorithm, known for its security and efficiency.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash the password before storing it in the database.
# This enhances security by storing a hashed version of the password.
def get_password_hash(password):
    """Generate a hash for the given password.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        str: A hashed version of the password.
    """
    return pwd_context.hash(password)