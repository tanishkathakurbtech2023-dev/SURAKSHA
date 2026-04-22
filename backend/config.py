import base64
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_env: str
    cors_origins: list[str]
    api_key: str
    encryption_key_b64: str
    ecdsa_private_key_pem: str
    ecdsa_public_key_pem: str
    db_path: str


DEFAULT_AES_KEY_B64 = base64.b64encode(b"0123456789abcdef0123456789abcdef").decode("utf-8")
DEFAULT_PRIVATE_KEY_PEM = """-----BEGIN PRIVATE KEY-----
MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgZaCeSHqo0KfW86tx
QnLi+ElnYItiVm8rDcP8YpvDGn2hRANCAAQ2Af6MNyN52jAb7fT7icJPdkhQ4W4L
aDScK5txR4e3YHriQBuQvSkAOLQ9vN3vWbWEtKNx6yovM2Pd4Qq8+n5L
-----END PRIVATE KEY-----"""
DEFAULT_PUBLIC_KEY_PEM = """-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAENgH+jDcjedowG+30+4nCT3ZIUOFu
C2g0nCubcUeHt2B64kAbkL0pADi0Pbzd71m1hLSjcesqLzNj3eEKvPp+Sw==
-----END PUBLIC KEY-----"""


def get_settings() -> Settings:
    cors = os.getenv("CORS_ORIGINS", "http://localhost:8000").split(",")
    return Settings(
        app_env=os.getenv("APP_ENV", "development"),
        cors_origins=[origin.strip() for origin in cors if origin.strip()],
        api_key=os.getenv("SURAKSHA_API_KEY", "dev-api-key"),
        encryption_key_b64=os.getenv("ENCRYPTION_KEY", DEFAULT_AES_KEY_B64),
        ecdsa_private_key_pem=os.getenv("ECDSA_PRIVATE_KEY_PEM", DEFAULT_PRIVATE_KEY_PEM),
        ecdsa_public_key_pem=os.getenv("ECDSA_PUBLIC_KEY_PEM", DEFAULT_PUBLIC_KEY_PEM),
        db_path=os.getenv("SQLITE_DB_PATH", "suraksha.db"),
    )
