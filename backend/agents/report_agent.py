class ReportDigestAgent:
    def generate(self, total: int, flagged: int, blocked: int) -> str:
        if total == 0:
            return "No transactions observed in the selected window."
        flagged_rate = round((flagged / total) * 100, 2)
        blocked_rate = round((blocked / total) * 100, 2)
        return (
            f"Processed {total} transactions. Flagged: {flagged} ({flagged_rate}%). "
            f"Blocked: {blocked} ({blocked_rate}%)."
        )
