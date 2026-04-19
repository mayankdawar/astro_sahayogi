"""Nuitka build script for cross-platform compilation."""
from __future__ import annotations
import subprocess
import platform
import sys


def build():
    system = platform.system()
    base_cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--enable-plugin=pyside6",
        "--include-data-dir=astro_sahayogi/ui/theme=astro_sahayogi/ui/theme",
        "--output-dir=dist",
        "--company-name=AstroSahayogi",
        "--product-name=Astro Sahayogi",
        "--file-version=1.0.0",
        "--product-version=1.0.0",
    ]

    if system == "Windows":
        base_cmd.extend([
            "--windows-icon-from-ico=astro_sahayogi/ui/theme/assets/icon.ico",
            "--windows-disable-console",
        ])
    elif system == "Darwin":
        base_cmd.extend([
            "--macos-create-app-bundle",
            "--macos-app-icon=astro_sahayogi/ui/theme/assets/icon.icns",
            "--macos-app-name=Astro Sahayogi",
        ])

    base_cmd.append("astro_sahayogi/main.py")

    print(f"Building for {system}...")
    print(" ".join(base_cmd))
    subprocess.run(base_cmd, check=True)
    print("Build complete! Output in dist/")


if __name__ == "__main__":
    build()
