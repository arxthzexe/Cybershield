import re

def has_tamil_script(text):
    return bool(re.search(r"[\u0B80-\u0BFF]", text))

def is_tanglish(text):
    words = [
        "enaku", "bayama", "romba",
        "panniten", "pannuvangala",
        "emaathitanga"
    ]
    return any(w in text.lower() for w in words)

def is_mixed(text):
    return has_tamil_script(text) and is_tanglish(text)

def response_style(text):
    if is_mixed(text): return "mixed"
    if has_tamil_script(text): return "tamil_spoken"
    if is_tanglish(text): return "tanglish"
    return "english"
