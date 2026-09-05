ENGLISH = [
    "scam", "fraud", "victim", "scared", "panic",
    "arrest", "police", "mistake", "help",
    "otp", "upi", "bank", "money", "link",
    "click", "download", "hacked", "stolen",
    "account", "password", "email", "sms",
    "message", "call", "unknown", "website",
    "phishing", "malware", "virus", "lost", "threat"
]

TANGLISH = [
    "bayama", "bayam", "enaku", "romba",
    "emaathitanga", "emathitanga",
    "thappu", "mistake", "panniten",
    "arrest", "police", "account",
    "otp", "upi", "bank"
]

TAMIL_SLANG = [
    "பயம்", "பயமா", "பயமாக",
    "ஏமாத்திட்டாங்க", "ஏமாந்தேன்",
    "தவறு", "தவறா பண்ணிட்டேன்",
    "போலீஸ்", "அரெஸ்ட்",
    "ஓடிபி", "யூபிஐ",
    "வங்கி", "அக்கவுண்ட்",
    "பணம்"
]

def is_victim_context(text: str) -> bool:
    lower = text.lower()
    if any(word in lower for word in ENGLISH): return True
    if any(word in lower for word in TANGLISH): return True
    if any(word in text for word in TAMIL_SLANG): return True
    return False
