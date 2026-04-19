"""Hardware fingerprint: machine-specific SHA-256 hash."""
from __future__ import annotations
import hashlib
import platform
import uuid


def get_hardware_fingerprint() -> str:
    """Compute a SHA-256 hash of MAC address + CPU identifier + platform."""
    mac = hex(uuid.getnode())
    cpu = platform.processor()
    system = platform.system()
    machine = platform.machine()
    raw = f"{mac}:{cpu}:{system}:{machine}"
    return hashlib.sha256(raw.encode()).hexdigest()
