"""Nuitka build script for cross-platform compilation.

Run from anywhere; paths are resolved from this file's location (repo root).
"""
from __future__ import annotations
import subprocess
import platform
import sys
from pathlib import Path


def _require_pyside6() -> None:
    """Nuitka's --enable-plugin=pyside6 uses this interpreter; PySide6 must be installed here."""
    try:
        import PySide6  # noqa: F401
    except ImportError as e:
        raise SystemExit(
            "PySide6 is not installed for the Python running this script. The Nuitka "
            "PySide6 plugin needs it. Install project deps, e.g.:\n"
            f"  {sys.executable} -m pip install -r requirements.txt\n"
            "(If you use a venv, activate it first, then run this build again.)"
        ) from e


def build():
    _require_pyside6()
    root = Path(__file__).resolve().parent.parent
    main_py = root / "main.py"
    theme_dir = root / "ui" / "theme"
    assets_dir = theme_dir / "assets"
    icon_icns = assets_dir / "icon.icns"
    icon_ico = assets_dir / "icon.ico"

    if not main_py.is_file():
        raise SystemExit(f"Expected entry script at {main_py}")

    system = platform.system()
    base_cmd = [
        sys.executable,
        "-m",
        "nuitka",
        "--standalone",
        "--onefile",
        "--enable-plugin=pyside6",
        f"--include-data-dir={theme_dir}=ui/theme",
        "--output-dir=dist",
        "--company-name=AstroSahayogi",
        "--product-name=Astro Sahayogi",
        "--file-version=1.0.0",
        "--product-version=1.0.0",
    ]

    if system == "Windows":
        if icon_ico.is_file():
            base_cmd.append(f"--windows-icon-from-ico={icon_ico}")
        base_cmd.append("--windows-disable-console")
    elif system == "Darwin":
        base_cmd.extend(
            [
                "--macos-create-app-bundle",
                "--macos-app-name=Astro Sahayogi",
            ]
        )
        if icon_icns.is_file():
            base_cmd.append(f"--macos-app-icon={icon_icns}")
        else:
            base_cmd.append("--macos-app-icon=none")

    base_cmd.append(str(main_py))

    print(f"Building for {system} from {root} ...")
    print(" ".join(base_cmd))
    subprocess.run(base_cmd, check=True, cwd=root)
    print("Build complete! Output in dist/")


if __name__ == "__main__":
    build()
