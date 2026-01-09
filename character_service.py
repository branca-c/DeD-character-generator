from typing import Dict, Any, List, Optional

from db import load_db, save_db
from gemini_client import generate_character_from_prompt, regenerate_backstory
from models import empty_character
from utils import new_id, now_iso


def create_character(user_prompt: str) -> Dict[str, Any]:
    ai_data = generate_character_from_prompt(user_prompt)

    c = empty_character()
    c["id"] = new_id()
    c["user_prompt"] = user_prompt
    c["name"] = ai_data["name"]
    c["race"] = ai_data["race"]
    c["class"] = ai_data["class"]
    c["level"] = ai_data["level"]
    c["stats"] = ai_data["stats"]
    c["backstory"] = ai_data["backstory"]
    c["physical_description"] = ai_data["physical_description"]
    c["created_at"] = now_iso()
    return c


def save_character(character: Dict[str, Any]) -> None:
    data = load_db()
    data["characters"].append(character)
    save_db(data)


def list_characters() -> List[Dict[str, Any]]:
    data = load_db()
    return data.get("characters", [])


def get_character(char_id: str) -> Optional[Dict[str, Any]]:
    for c in list_characters():
        if c.get("id") == char_id:
            return c
    return None


def delete_character(char_id: str) -> bool:
    data = load_db()
    chars = data.get("characters", [])
    new_chars = [c for c in chars if c.get("id") != char_id]
    if len(new_chars) == len(chars):
        return False
    data["characters"] = new_chars
    save_db(data)
    return True


def regenerate_backstory_for_id(char_id: str) -> Dict[str, Any]:
    data = load_db()
    chars = data.get("characters", [])

    for i, c in enumerate(chars):
        if c.get("id") == char_id:
            new_story = regenerate_backstory(c)
            chars[i]["backstory"] = new_story
            save_db(data)
            return chars[i]

    raise ValueError("Personaggio non trovato.")
