import uuid
from datetime import datetime, timezone


def new_id() -> str:
    return str(uuid.uuid4())


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def clamp_int(n: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, int(n)))


def stat_bar(value: int, width: int = 10) -> str:
    """
    Barra visuale: value 0..20 circa. Qui usiamo 3..18 come da consegna.
    """
    value = clamp_int(value, 3, 18)
    filled = round((value - 3) / (18 - 3) * width)
    filled = clamp_int(filled, 0, width)
    return "█" * filled + "░" * (width - filled)


def safe_int(x, fallback: int) -> int:
    try:
        return int(x)
    except Exception:
        return fallback
