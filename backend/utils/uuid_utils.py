import uuid


def generate_uuid() -> str:
    """Generates a standard UUID v4 string."""
    return str(uuid.uuid4())


def generate_token_id(prefix: str = "FIN-2026") -> str:
    """Generates an enterprise investigation token ID string (e.g. FIN-2026-88A92)."""
    short_hash = uuid.uuid4().hex[:6].upper()
    return f"{prefix}-{short_hash}"
