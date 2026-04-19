"""License key validator: checks key against local hardware fingerprint."""
from __future__ import annotations
import os
import json
from astro_sahayogi.services.license.fingerprint import get_hardware_fingerprint
from astro_sahayogi.services.license.keygen import generate_license_key

LICENSE_FILE = "astro_sahayogi_license.json"


class LicenseValidator:
    def __init__(self, license_path: str | None = None):
        self._path = license_path or LICENSE_FILE

    def is_licensed(self) -> bool:
        if not os.path.exists(self._path):
            return False
        try:
            with open(self._path, "r") as f:
                data = json.load(f)
            stored_key = data.get("license_key", "")
            fp = get_hardware_fingerprint()
            expected = generate_license_key(fp)
            return stored_key == expected
        except Exception:
            return False

    def activate(self, key: str) -> bool:
        fp = get_hardware_fingerprint()
        expected = generate_license_key(fp)
        if key == expected:
            with open(self._path, "w") as f:
                json.dump({"license_key": key, "fingerprint": fp}, f)
            return True
        return False

    def get_fingerprint(self) -> str:
        return get_hardware_fingerprint()
