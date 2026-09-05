from url_scanner.hybrid_url_risk import analyze_url

url = input("Enter URL to scan: ")
result = analyze_url(url)

print("\nScan Result:")
for k, v in result.items():
    print(f"{k}: {v}")
