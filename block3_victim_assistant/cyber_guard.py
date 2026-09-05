CYBER_KEYWORDS = [
    "scam", "fraud", "otp", "phishing", "upi", "bank",
    "hack", "hacked", "malware", "virus", "cyber",
    "account", "password", "link", "sms", "whatsapp"
]

def is_cyber_related(text: str) -> bool:
    text = text.lower()
    return any(word in text for word in CYBER_KEYWORDS)
