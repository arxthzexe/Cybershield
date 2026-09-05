import os
from intent_detector import is_victim_context
from language_style import response_style
from reassurance import reassurance
from llm_engine import ask_llm

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYSTEM_PROMPT = open(
    os.path.join(BASE_DIR, "system_prompt.txt"),
    encoding="utf-8"
).read()

def get_response(user_input):
    if not is_victim_context(user_input):
        return "⚠️ I assist only with cybersecurity and online safety concerns."

    style = response_style(user_input)
    llm_reply = ask_llm(user_input, style, SYSTEM_PROMPT)

    footer = (
        "\n\n🛡️ Important Safety Steps:\n"
        "• Never share OTP / PIN\n"
        "• Stop responding to scammers\n"
        "• Call 1930 (India Cyber Helpline)\n"
        "• Visit cybercrime.gov.in"
    )

    return reassurance(style) + llm_reply + footer
