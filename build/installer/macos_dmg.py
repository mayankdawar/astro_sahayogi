"""macOS DMG creator wrapper using create-dmg."""
from __future__ import annotations
import subprocess
import sys


def create_dmg():
    cmd = [
        "create-dmg",
        "--volname", "Astro Sahayogi",
        "--window-pos", "200", "120",
        "--window-size", "600", "400",
        "--icon-size", "100",
        "--app-drop-link", "425", "170",
        "dist/AstroSahayogi.dmg",
        "dist/main.app",
    ]
    print("Creating DMG...")
    subprocess.run(cmd, check=True)
    print("DMG created at dist/AstroSahayogi.dmg")


if __name__ == "__main__":
    create_dmg()
