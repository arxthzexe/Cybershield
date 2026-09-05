def reassurance(style):
    if style in ["tamil_spoken", "mixed"]:
        return "உங்களுக்கு பயம் வருவது புரியுது. தயவு செய்து அமைதியாக இருங்கள்.\n\n"
    if style == "tanglish":
        return "Enaku puriyuthu, idhu romba scary situation.\n\n"
    return "I understand why you're scared. Please stay calm.\n\n"
