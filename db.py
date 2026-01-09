import json
import os
from typing import Dict, Any
from models import empty_db

DB_FILE = "db.json"


def ensure_db_exists() -> None:
    if not os.path.exists(DB_FILE):
        save_db(empty_db())


def load_db() -> Dict[str, Any]:
    ensure_db_exists()
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # db rotto -> ripartiamo vuoto
        return empty_db()
    except Exception:
        return empty_db()


def save_db(data: Dict[str, Any]) -> None:
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
