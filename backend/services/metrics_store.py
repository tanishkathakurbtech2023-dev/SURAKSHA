from dataclasses import dataclass

from backend.db import get_conn


@dataclass
class Metrics:
    total_transactions: int
    blocked_transactions: int
    flagged_transactions: int


class MetricsStore:
    def record(self, flagged: bool, blocked: bool) -> Metrics:
        with get_conn() as conn:
            conn.execute(
                """
                UPDATE metrics
                SET total_transactions = total_transactions + 1,
                    blocked_transactions = blocked_transactions + ?,
                    flagged_transactions = flagged_transactions + ?
                WHERE id = 1
                """,
                (1 if blocked else 0, 1 if flagged else 0),
            )
            row = conn.execute(
                "SELECT total_transactions, blocked_transactions, flagged_transactions FROM metrics WHERE id = 1"
            ).fetchone()
        return Metrics(**dict(row))

    def snapshot(self) -> Metrics:
        with get_conn() as conn:
            row = conn.execute(
                "SELECT total_transactions, blocked_transactions, flagged_transactions FROM metrics WHERE id = 1"
            ).fetchone()
        return Metrics(**dict(row))


metrics_store = MetricsStore()
