import google.generativeai as genai
import json
import os
from typing import Dict, Any, Optional
# Placeholder for API Key setup. 
# Ideally, this should be in an env variable.
# We will try to get it from env, or warn user.
def configure_api():
    """Configures the Gemini API."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        # For this specific environment, we might checking the user provided input or just fail gracefully
        # Assuming the user has set it up or will set it up.
        pass
    if api_key:
        genai.configure(api_key=api_key)
def generate_character_data(description: str) -> Optional[Dict[str, Any]]:
    """Generates character data from a description using Gemini."""
    configure_api()
    
    prompt = f"""
    You are a D&D 5e Character Generator. 
    Create a complete character based on this description: "{description}".
    
    Return ONLY a valid JSON object with the following structure:
    {{
        "name": "Character Name",
        "race": "Race",
        "class": "Class",
        "level": 1,
        "stats": {{
            "strength": 10,
            "dexterity": 10,
            "constitution": 10,
            "intelligence": 10,
            "wisdom": 10,
            "charisma": 10
        }},
        "backstory": "A short backstory...",
        "physical_description": "A short physical description..."
    }}
    
    Ensure stats are appropriate for the class and race (3-18 range).
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        # Clean up the response to ensure it's valid JSON
        text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        return data
    except Exception as e:
        print(f"\n❌ Error generating character: {e}")
        return None
def generate_backstory(character: Dict[str, Any]) -> Optional[str]:
    """Regenerates the backstory for a character."""
    configure_api()
    
    prompt = f"""
    Rewrite the backstory for this D&D character:
    Name: {character.get('name')}
    Race: {character.get('race')}
    Class: {character.get('class')}
    Current Backstory: {character.get('backstory')}
    
    Write a NEW, creative backstory (max 200 words). Return ONLY the text of the backstory.
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"\n❌ Error regenerating backstory: {e}")
        return None
