"""License key generator (seller-side tool).

Usage: python -m astro_sahayogi.services.license.keygen <fingerprint>
"""
from __future__ import annotations
import hmac
import hashlib
import sys

SECRET = b"AstroSahayogi_LK_2025_Secret_Key"


def generate_license_key(fingerprint: str) -> str:
    """Generate an HMAC-SHA256 license key from a hardware fingerprint."""
    return hmac.new(SECRET, fingerprint.encode(), hashlib.sha256).hexdigest()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m astro_sahayogi.services.license.keygen <fingerprint>")
        sys.exit(1)
    fp = sys.argv[1]
    key = generate_license_key(fp)
    print(f"Fingerprint: {fp}")
    print(f"License Key: {key}")
