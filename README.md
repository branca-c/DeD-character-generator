# 🐉 D&D Character Generator CLI

Un'applicazione **CLI in Python** per generare personaggi di **Dungeons & Dragons** a partire da una descrizione testuale dell’utente, utilizzando l’API **Gemini**.

L’utente descrive il personaggio desiderato e l’app genera automaticamente **nome, razza, classe, statistiche, backstory e descrizione fisica**, con possibilità di salvare e gestire i personaggi creati.

---

## 🎯 Obiettivo del progetto

- Creare un'app da terminale per generare personaggi D&D
- Usare **Gemini API** per la generazione dei contenuti
- Salvare i personaggi in un file locale `db.json`
- Fornire un’interfaccia CLI semplice, leggibile e guidata

---

## ⚙️ Funzionalità principali

### 🧙 Generazione personaggi
- Generazione di un personaggio a partire da una descrizione testuale
- Output completo:
  - Nome
  - Razza
  - Classe
  - Statistiche (FOR, DES, COS, INT, SAG, CAR)
  - Backstory
  - Descrizione fisica
- Statistiche coerenti con razza e classe
- Possibilità di rigenerare un personaggio con una nuova descrizione

### 📦 Gestione personaggi
- Salvataggio automatico in `db.json`
- Visualizzazione lista personaggi salvati
- Visualizzazione dettaglio di un personaggio
- Eliminazione di un personaggio
- Rigenerazione **solo della backstory** di un personaggio esistente

---

## 🗂️ Struttura dati

I personaggi sono salvati in formato JSON:

```json
{
  "characters": [
    {
      "id": "uuid",
      "user_prompt": "un mago misterioso con un passato oscuro",
      "name": "Eldrin Moonwhisper",
      "race": "Elfo",
      "class": "Mago",
      "level": 1,
      "stats": {
        "strength": 8,
        "dexterity": 14,
        "constitution": 12,
        "intelligence": 17,
        "wisdom": 13,
        "charisma": 10
      },
      "backstory": "Nato nella biblioteca di Silverymoon...",
      "physical_description": "Alto e slanciato, capelli argentati...",
      "created_at": "2025-01-09T10:30:00"
    }
  ]
}
