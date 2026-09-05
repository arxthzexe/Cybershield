from malware_scanner.hybrid_apk_risk import analyze_apk

# Dummy extracted APK info (later automated)
apk_info = {
    "permissions": [
        "READ_SMS",
        "INTERNET",
        "SYSTEM_ALERT_WINDOW"
    ]
}

apk_path = input("Enter APK file path: ")

result = analyze_apk(apk_info, apk_path)

print("\nAPK Scan Result:")
for k, v in result.items():
    print(f"{k}: {v}")
