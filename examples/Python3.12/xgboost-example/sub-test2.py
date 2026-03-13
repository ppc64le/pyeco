import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

print("✅ Sub-test 2: Cryptography + Requests")

# Generate RSA key and sign a message
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
message = b"Sub-test message 2"
signature = key.sign(message, padding.PKCS1v15(), hashes.SHA256())
key.public_key().verify(signature, message, padding.PKCS1v15(), hashes.SHA256())
print("Message signed and verified successfully")

# Send message via HTTP
response = requests.post("https://httpbin.org/post", data=message)
