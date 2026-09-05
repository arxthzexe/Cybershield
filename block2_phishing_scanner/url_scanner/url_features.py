import re
import tldextract
import validators
from urllib.parse import urlparse

def extract_url_features(url):
    parsed = urlparse(url)
    ext = tldextract.extract(url)

    suspicious_keywords = [
        "login", "verify", "update", "secure", "bank",
        "upi", "payment", "confirm", "account"
    ]

    return {
        "url_length": len(url),
        "has_ip": int(bool(re.search(r"\d+\.\d+\.\d+\.\d+", url))),
        "has_https": int(parsed.scheme == "https"),
        "num_dots": url.count("."),
        "num_hyphens": url.count("-"),
        "num_slashes": url.count("/"),
        "has_at": int("@" in url),
        "keyword_count": sum(word in url.lower() for word in suspicious_keywords),
        "domain_length": len(ext.domain),
        "subdomain_length": len(ext.subdomain),
        "is_valid_url": 1 if validators.url(url) == True else 0
    }
