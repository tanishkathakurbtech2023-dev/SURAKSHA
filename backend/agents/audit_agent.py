from backend.security.audit_log import audit_chain


class AuditQueryAgent:
    def query(self, search: str) -> list[dict[str, str]]:
        search_l = search.lower().strip()
        entries = []
        for entry in audit_chain.all():
            serialized = f"{entry.event} {entry.payload}".lower()
            if search_l in serialized:
                entries.append(entry.__dict__)
        return entries
