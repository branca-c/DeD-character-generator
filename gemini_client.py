import json
from typing import Dict, Any, Optional

from google import genai

from models import character_schema
from utils import clamp_int


MODEL_NAME = "gemini-2.5-flash"  # modello usato nella quickstart ufficiale :contentReference[oaicite:2]{index=2}


def _parse_json_maybe(text: str) -> Dict[str, Any]:
    """
    Prova a parsare JSON puro. Se Gemini restituisce spazi/newline è ok.
    """
    return json.loads(text)


def _normalize_character(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizza e mette in sicurezza i valori (stats 3..18, level >=1).
    """
    stats = data.get("stats", {}) or {}
    fixed_stats = {
        "strength": clamp_int(stats.get("strength", 10), 3, 18),
        "dexterity": clamp_int(stats.get("dexterity", 10), 3, 18),
        "constitution": clamp_int(stats.get("constitution", 10), 3, 18),
        "intelligence": clamp_int(stats.get("intelligence", 10), 3, 18),
        "wisdom": clamp_int(stats.get("wisdom", 10), 3, 18),
        "charisma": clamp_int(stats.get("charisma", 10), 3, 18),
    }

    level = data.get("level", 1)
    try:
        level = int(level)
    except Exception:
        level = 1
    if level < 1:
        level = 1

    return {
        "name": str(data.get("name", "")).strip(),
        "race": str(data.get("race", "")).strip(),
        "class": str(data.get("class", "")).strip(),
        "level": level,
        "stats": fixed_stats,
        "backstory": str(data.get("backstory", "")).strip(),
        "physical_description": str(data.get("physical_description", "")).strip(),
    }


def generate_character_from_prompt(user_prompt: str) -> Dict[str, Any]:
    """
    Chiama Gemini e chiede un JSON strutturato per creare un personaggio.
    """
    client = genai.Client()

    system_rules = (
        "Sei un generatore di personaggi Dungeons & Dragons.\n"
        "Regole:\n"
        "- Rispondi SOLO con JSON valido.\n"
        "- stats: valori interi tra 3 e 18.\n"
        "- Le stats devono essere coerenti con razza e classe (es. Mago -> INT alta).\n"
        "- backstory e descrizione fisica in italiano.\n"
        "- level deve essere 1.\n"
    )

    prompt = (
        f"{system_rules}\n"
        f"Descrizione utente: {user_prompt}\n"
        "Genera un personaggio completo seguendo lo schema."
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": character_schema(),
            },
        )
    except Exception as e:
        raise RuntimeError(f"API non raggiungibile o errore Gemini: {e}")

    # Con lo schema, spesso trovi già response.parsed; se non c'è, parsami response.text.
    data: Optional[Dict[str, Any]] = None
    if getattr(response, "parsed", None):
        try:
            data = dict(response.parsed)
        except Exception:
            data = None

    if data is None:
        try:
            data = _parse_json_maybe(response.text)
        except Exception:
            raise RuntimeError("Risposta non valida: Gemini non ha restituito JSON parsabile.")

    return _normalize_character(data)


def regenerate_backstory(character: Dict[str, Any]) -> str:
    """
    Rigenera SOLO la backstory partendo dai campi del personaggio già salvato.
    """
    client = genai.Client()

    prompt = (
        "Scrivi SOLO la backstory in italiano (testo semplice, max 1200 caratteri).\n"
        "Mantieni coerenti razza, classe, stats e descrizione fisica.\n\n"
        f"Nome: {character.get('name')}\n"
        f"Razza: {character.get('race')}\n"
        f"Classe: {character.get('class')}\n"
        f"Stats: {character.get('stats')}\n"
        f"Descrizione fisica: {character.get('physical_description')}\n"
    )

    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    except Exception as e:
        raise RuntimeError(f"API non raggiungibile o errore Gemini: {e}")

    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini non ha generato una backstory valida.")
    return text
