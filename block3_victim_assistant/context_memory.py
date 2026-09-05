class ContextMemory:
    def __init__(self):
        self.flags = {
            "otp_requested": False,
            "bank_related": False,
            "urgency_detected": False
        }

    def update(self, intent):
        if intent == "asks_for_otp":
            self.flags["otp_requested"] = True
        elif intent == "bank_claim":
            self.flags["bank_related"] = True
        elif intent == "urgent_pressure":
            self.flags["urgency_detected"] = True
