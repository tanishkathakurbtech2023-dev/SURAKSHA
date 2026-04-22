import sqlite3

from backend.db import get_conn


class NonceStore:
    def use_nonce(self, nonce: str) -> bool:
        try:
            with get_conn() as conn:
                conn.execute("INSERT INTO used_nonces (nonce) VALUES (?)", (nonce,))
            return True
        except sqlite3.IntegrityError:
            return False


nonce_store = NonceStore()
