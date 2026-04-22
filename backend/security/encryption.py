import base64
import json
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from backend.config import get_settings


def encrypt_payload(plaintext: str) -> str:
    """AES-256-GCM encryption.

    Returns a base64-encoded JSON envelope containing nonce and ciphertext.
    """
    settings = get_settings()
    key = base64.b64decode(settings.encryption_key_b64)
    if len(key) != 32:
        raise ValueError("ENCRYPTION_KEY must be base64 for exactly 32 bytes")

    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)

    envelope = {
        "nonce": base64.b64encode(nonce).decode("utf-8"),
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
    }
    return base64.b64encode(json.dumps(envelope).encode("utf-8")).decode("utf-8")
