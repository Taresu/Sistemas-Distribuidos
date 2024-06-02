from base64 import b64decode

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
...
-----END PUBLIC KEY-----
"""

def verify_signature(message, signature):
    key = RSA.import_key(PUBLIC_KEY)
    h = SHA256.new(message.encode('utf-8'))
    try:
        pkcs1_15.new(key).verify(h, b64decode(signature))
        return True
    except (ValueError, TypeError):
        return False