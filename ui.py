from typing import Dict, Any, List

from utils import stat_bar


CLASS_EMOJI = {
    "guerriero": "⚔️",
    "mago": "🧙",
    "chierico": "⛪",
    "ladro": "🗡️",
    "ranger": "🏹",
    "barbaro": "🪓",
    "bardo": "🎻",
    "druido": "🌿",
    "paladino": "🛡️",
    "monaco": "🥋",
    "stregone": "✨",
    "warlock": "📜",
}

RACE_EMOJI = {
    "elfo": "🧝",
    "nano": "⛏️",
    "umano": "🧑",
    "halfling": "🍀",
    "gnomo": "🧠",
    "tiefling": "😈",
    "orco": "🧌",
    "mezzelfo": "🧝",
}


def _pick_emoji(mapping: Dict[str, str], text: str) -> str:
    t = (text or "").strip().lower()
    for k, v in mapping.items():
        if k in t:
            return v
    return "🎲"


def header(title: str) -> None:
    print("\n" + "=" * 54)
    print(f"🎲  {title}")
    print("=" * 54)


def menu() -> None:
    print("\nScegli un'opzione:")
    print("1) ✨ Genera nuovo personaggio")
    print("2) 📜 Lista personaggi salvati")
    print("3) 🔎 Dettaglio personaggio (ID)")
    print("4) 🗑️  Cancella personaggio (ID)")
    print("5) 📝 Rigenera SOLO backstory (ID)")
    print("0) 🚪 Esci")


def ask(prompt: str) -> str:
    return input(f"\n{prompt} ").strip()


def show_character(c: Dict[str, Any]) -> None:
    cls = c.get("class", "")
    race = c.get("race", "")
    e_cls = _pick_emoji(CLASS_EMOJI, cls)
    e_race = _pick_emoji(RACE_EMOJI, race)

    header(f"{c.get('name')}  {e_race}{e_cls}")
    print(f"🆔 ID: {c.get('id')}")
    print(f"🗓️ Creato: {c.get('created_at')}")
    print(f"🧩 Prompt utente: {c.get('user_prompt')}")
    print(f"\n🏷️ Razza: {race}")
    print(f"🎖️ Classe: {cls} (Lv {c.get('level', 1)})")

    s = c.get("stats", {}) or {}
    print("\n📊 Stats")
    _print_stat("FOR", s.get("strength", 10))
    _print_stat("DES", s.get("dexterity", 10))
    _print_stat("COS", s.get("constitution", 10))
    _print_stat("INT", s.get("intelligence", 10))
    _print_stat("SAG", s.get("wisdom", 10))
    _print_stat("CAR", s.get("charisma", 10))

    print("\n📖 Backstory")
    print(c.get("backstory", "-"))

    print("\n🧍 Descrizione fisica")
    print(c.get("physical_description", "-"))


def _print_stat(label: str, value: int) -> None:
    bar = stat_bar(int(value))
    print(f"{label:>3}: {bar}  {int(value)}")


def show_list(chars: List[Dict[str, Any]]) -> None:
    header("Personaggi salvati")
    if not chars:
        print("😶 Nessun personaggio salvato.")
        return

    for i, c in enumerate(chars, start=1):
        cls = c.get("class", "")
        race = c.get("race", "")
        e = _pick_emoji(RACE_EMOJI, race) + _pick_emoji(CLASS_EMOJI, cls)
        print(f"{i:>2}. {e} {c.get('name')} — {race}, {cls} — ID: {c.get('id')}")
