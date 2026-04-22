import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

from backend.config import get_settings


def sign_transaction(payload: str) -> str:
    settings = get_settings()
    private_key = serialization.load_pem_private_key(
        settings.ecdsa_private_key_pem.encode("utf-8"), password=None
    )
    signature = private_key.sign(payload.encode("utf-8"), ec.ECDSA(hashes.SHA256()))
    return base64.b64encode(signature).decode("utf-8")


def verify_signature(payload: str, signature_b64: str) -> bool:
    settings = get_settings()
    public_key = serialization.load_pem_public_key(settings.ecdsa_public_key_pem.encode("utf-8"))
    try:
        public_key.verify(base64.b64decode(signature_b64), payload.encode("utf-8"), ec.ECDSA(hashes.SHA256()))
        return True
    except Exception:
        return False
