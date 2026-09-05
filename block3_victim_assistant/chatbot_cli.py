from chatbot_manager import get_response

print("🛡️ CyberShield: I assist with cybersecurity and online safety.")

while True:
    msg = input("\nYou: ")
    if msg.lower() in ["exit", "quit"]:
        break
    reply = get_response(msg)
    print("\nCyberShield:", reply)
