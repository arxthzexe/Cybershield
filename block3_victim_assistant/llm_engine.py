import requests
import json

def get_fallback_guidance(style):
    if style in ["tamil_spoken", "mixed"]:
        return "உங்கள் பணத்தையோ அல்லது OTP-யையோ யாருடனும் பகிர வேண்டாம். உடனடியாக உங்கள் வங்கியைத் தொடர்புகொள்ளவும்."
    elif style == "tanglish":
        return "Bayam padadhinga, immediate-ah ungalla bank-u call panni card/account block panna sollunga. OTP shared panna koodadhu."
    else:
        return "Do not panic. Immediately contact your bank to freeze your card or account. Never share OTP or PIN with anyone."

def ask_llm(user_input, style, system_prompt):
    style_map = {
        "english": "Respond in simple, empathetic English.",
        "tanglish": "Respond in simple spoken Tanglish, focusing on reassurance.",
        "tamil_spoken": "Respond in spoken Tamil using Tamil script, showing empathy.",
        "mixed": "Respond in mixed spoken Tamil and English, maintaining a calm tone."
    }

    # Fallback if style isn't found
    style_instruction = style_map.get(style, style_map["english"])
    prompt = f"{system_prompt}\n\nINSTRUCTION: {style_instruction}\nUSER: {user_input}\nASSISTANT:"

    payload = {
        "model": "llama3:latest",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.4,
            "top_p": 0.9
        }
    }

    try:
        response = requests.post("http://127.0.0.1:11434/api/generate", json=payload, timeout=8)
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            return get_fallback_guidance(style)
    except requests.exceptions.RequestException:
        return get_fallback_guidance(style)

