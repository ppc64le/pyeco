import bcrypt

def hash_password(password: str) -> bytes:
    """
    Hashes a plaintext password using bcrypt.
    """
    # Convert password to bytes
    password_bytes = password.encode('utf-8')

    # Generate salt
    salt = bcrypt.gensalt()

    # Create hashed password
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed


def verify_password(password: str, hashed: bytes) -> bool:
    """
    Verifies a plaintext password against a hashed one.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed)


if __name__ == "__main__":
    # Sample password
    plain_password = "MySecurePassword123"

    # Hash the password
    hashed_password = hash_password(plain_password)
    print(f"Plain Password: {plain_password}")
    print(f"Hashed Password: {hashed_password.decode('utf-8')}")

    # Verify password (correct one)
    is_correct = verify_password("MySecurePassword123", hashed_password)
    print("Password verification (correct):", is_correct)

    # Verify password (wrong one)
    is_wrong = verify_password("WrongPassword", hashed_password)
    print("Password verification (wrong):", is_wrong)
