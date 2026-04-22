import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone

from backend.db import get_conn


@dataclass
class AuditEntry:
    timestamp: str
    event: str
    payload: str
    prev_hash: str
    hash: str


class AuditChain:
    def _compute_hash(self, timestamp: str, event: str, payload: str, prev_hash: str) -> str:
        raw = f"{timestamp}|{event}|{payload}|{prev_hash}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def append(self, event: str, payload: str) -> AuditEntry:
        with get_conn() as conn:
            row = conn.execute("SELECT hash FROM audit_chain ORDER BY id DESC LIMIT 1").fetchone()
            prev_hash = row["hash"] if row else "GENESIS"
            timestamp = datetime.now(timezone.utc).isoformat()
            current_hash = self._compute_hash(timestamp, event, payload, prev_hash)
            conn.execute(
                """
                INSERT INTO audit_chain (timestamp, event, payload, prev_hash, hash)
                VALUES (?, ?, ?, ?, ?)
                """,
                (timestamp, event, payload, prev_hash, current_hash),
            )
        return AuditEntry(timestamp=timestamp, event=event, payload=payload, prev_hash=prev_hash, hash=current_hash)

    def all(self) -> list[AuditEntry]:
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT timestamp, event, payload, prev_hash, hash FROM audit_chain ORDER BY id ASC"
            ).fetchall()
        return [AuditEntry(**dict(row)) for row in rows]


audit_chain = AuditChain()
