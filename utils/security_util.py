from model.usuario import Usuario
import binascii
import os
import hashlib

LENGHT_STRING_TOKEN = 20


def create_token() -> str:
    return binascii.hexlify(os.urandom(LENGHT_STRING_TOKEN)).decode()


def hashed_value(some_string: str) -> str:
    sha_signature = hashlib.sha256(some_string.encode()).hexdigest()
    return sha_signature
