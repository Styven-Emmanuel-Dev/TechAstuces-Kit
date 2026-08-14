"""headers.py — HTTP security headers scanner."""

import requests

CHECKS = {
    "Strict-Transport-Security": "Forces HTTPS (HSTS) — protects against downgrade to HTTP",
    "Content-Security-Policy": "Restricts script/content sources (XSS protection)",
    "X-Frame-Options": "Prevents clickjacking (site embedded in a malicious iframe)",
    "X-Content-Type-Options": "Stops the browser from guessing file types (MIME sniffing)",
    "Referrer-Policy": "Controls info sent to the next site when a link is clicked",
    "Permissions-Policy": "Restricts access to features (camera, mic, geolocation...)",
}


def run(url: str):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    print(f"🔍 Scanning {url}\n")

    try:
        res = requests.get(url, timeout=10, allow_redirects=True)
    except requests.RequestException as e:
        print(f"❌ Could not reach this site: {e}")
        return

    if url.startswith("https://"):
        print("✅ HTTPS active")
    else:
        print("🔴 No HTTPS — all data travels in plain text")

    score = 0
    total = len(CHECKS)

    for header, explanation in CHECKS.items():
        present = header in res.headers
        icon = "✅" if present else "🔴"
        print(f"{icon} {header}")
        print(f"   {explanation}")
        if present:
            score += 1
            print(f"   Value: {res.headers[header][:80]}")
        print()

    percent = round((score / total) * 100)
    print(f"Score: {score}/{total} headers present ({percent}%)")

    if percent >= 80:
        print("🟢 Good security configuration.")
    elif percent >= 40:
        print("🟡 Decent, but there's room for improvement.")
    else:
        print("🔴 Weak configuration — several basic protections are missing.")
