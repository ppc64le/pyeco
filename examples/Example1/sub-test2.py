import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta, timezone

# Generate RSA key pair
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

private_key = key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

public_key = key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Create a JWT with timezone-aware UTC expiration
payload = {
    "user": "gerrit",
    "role": "tester",
    "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
}

encoded_jwt = jwt.encode(payload, private_key, algorithm="RS256")

# Decode and verify JWT
try:
    decoded = jwt.decode(encoded_jwt, public_key, algorithms=["RS256"])
    print("JWT verification passed. Payload:")
    print(decoded)
except jwt.exceptions.InvalidTokenError as e:
    print("JWT verification failed:", str(e))
