"""passcheck.py — password strength auditor + Have I Been Pwned check.

Uses the HIBP k-anonymity API: only the first 5 chars of the SHA1 hash
are ever sent over the network — the real password never leaves your device.
"""

import getpass
import hashlib
import math
import requests


def estimate_entropy(password: str) -> float:
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(not c.isalnum() for c in password):
        pool += 32
    if pool == 0:
        return 0.0
    return len(password) * math.log2(pool)


def crack_time_estimate(entropy_bits: float) -> str:
    # Rough estimate assuming 10 billion guesses/sec (modern GPU rig)
    guesses = 2 ** entropy_bits
    seconds = guesses / 10_000_000_000

    if seconds < 1:
        return "instant"
    if seconds < 60:
        return f"{seconds:.0f} seconds"
    if seconds < 3600:
        return f"{seconds/60:.0f} minutes"
    if seconds < 86400:
        return f"{seconds/3600:.0f} hours"
    if seconds < 31536000:
        return f"{seconds/86400:.0f} days"
    years = seconds / 31536000
    if years > 1_000_000:
        return "millions of years"
    return f"{years:,.0f} years"


def check_hibp(password: str):
    """Returns how many times this password appeared in known breaches, or None on error."""
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]

    try:
        res = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=8)
        res.raise_for_status()
    except requests.RequestException:
        return None

    for line in res.text.splitlines():
        h, count = line.split(":")
        if h == suffix:
            return int(count)
    return 0


COMMON_PATTERNS = ["123456", "password", "azerty", "qwerty", "letmein", "admin", "welcome"]


def run():
    print("🔐 Password Strength Auditor\n")
    password = getpass.getpass("Enter the password to test (hidden): ")

    if not password:
        print("No password entered.")
        return

    entropy = estimate_entropy(password)
    crack_time = crack_time_estimate(entropy)

    print(f"\nLength          : {len(password)} characters")
    print(f"Entropy          : {entropy:.1f} bits")
    print(f"Estimated crack time (brute-force attack): {crack_time}")

    lowered = password.lower()
    weak_pattern = next((p for p in COMMON_PATTERNS if p in lowered), None)
    if weak_pattern:
        print(f"⚠️  Contains a very common pattern: '{weak_pattern}'")

    print("\nChecking known breaches (Have I Been Pwned)...")
    count = check_hibp(password)

    if count is None:
        print("⚠️  Could not reach the HIBP API — try again later.")
    elif count == 0:
        print("✅ Not found in any known breach.")
    else:
        print(f"🔴 This password appeared {count:,} times in known data breaches — change it.")

    if entropy < 40:
        verdict = "🔴 Weak"
    elif entropy < 60:
        verdict = "🟡 Medium"
    else:
        verdict = "🟢 Strong"
    print(f"\nOverall verdict: {verdict}")
