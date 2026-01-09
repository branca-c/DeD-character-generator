from typing import Dict, Any


def empty_db() -> Dict[str, Any]:
    return {"characters": []}


def empty_character() -> Dict[str, Any]:
    return {
        "id": "",
        "user_prompt": "",
        "name": "",
        "race": "",
        "class": "",
        "level": 1,
        "stats": {
            "strength": 10,
            "dexterity": 10,
            "constitution": 10,
            "intelligence": 10,
            "wisdom": 10,
            "charisma": 10,
        },
        "backstory": "",
        "physical_description": "",
        "created_at": "",
    }


def character_schema() -> Dict[str, Any]:
    """
    JSON Schema (in forma dict) per chiedere a Gemini un output strutturato.
    """
    return {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "race": {"type": "string"},
            "class": {"type": "string"},
            "level": {"type": "integer"},
            "stats": {
                "type": "object",
                "properties": {
                    "strength": {"type": "integer"},
                    "dexterity": {"type": "integer"},
                    "constitution": {"type": "integer"},
                    "intelligence": {"type": "integer"},
                    "wisdom": {"type": "integer"},
                    "charisma": {"type": "integer"},
                },
                "required": [
                    "strength",
                    "dexterity",
                    "constitution",
                    "intelligence",
                    "wisdom",
                    "charisma",
                ],
            },
            "backstory": {"type": "string"},
            "physical_description": {"type": "string"},
        },
        "required": ["name", "race", "class", "level", "stats", "backstory", "physical_description"],
    }
