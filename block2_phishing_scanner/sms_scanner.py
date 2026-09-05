from text_scanner.hybrid_text_risk import analyze_text

if __name__ == "__main__":
    msg = input("Enter SMS / WhatsApp message:\n")
    
    result = analyze_text(msg)

    print("\nScan Result:")
    for key, value in result.items():
        print(f"{key}: {value}")
