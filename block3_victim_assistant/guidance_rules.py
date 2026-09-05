def give_guidance(ctx):
    advice = ["⚠ Safety Guidance:"]

    if ctx["otp_requested"]:
        advice.append("- Do NOT share OTP with anyone.")

    if ctx["bank_related"]:
        advice.append("- Banks will NEVER ask you for verification links.")

    if ctx["urgency_detected"]:
        advice.append("- Scammers use urgency to trick victims.")

    if not any(ctx.values()):
        advice.append("- So far nothing looks dangerous.")

    advice.append("\nIf uncertain, call 1930 (Cyber Helpline).")
    return advice
