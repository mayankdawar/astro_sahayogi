# Astro Sahayogi

**KP Astrology Professional Suite** — a cross-platform desktop application for Krishnamurti Paddhati (KP) astrology, built with **PySide6** and **Swiss Ephemeris** (`pyswisseph`).

## Features

- Full KP astrology: planetary positions, cusps, Nadi significators, Vimshottari Dasha (5 levels)
- North Indian diamond chart with Lagna, Bhava Chalit, and Lal Kitab Varshphal
- Live Ruling Planets (RP) with 1-second refresh
- Advanced tools: Forward Check, S-Sub Tracker, Degree Hits, Retro Report, Transit Search, Auto-BTR
- Medical astrology, intraday and long-term market predictors
- Astro Vastu with planet-to-cusp, planet-to-planet, and house-to-house aspects
- Bilingual: English and Hindi
- Hardware-fingerprint licensing for commercial distribution
- Nuitka-compiled native binaries (no Python runtime needed for distributed builds)

## Requirements

- **Python 3.11+** (recommended; matches tooling such as Graphify in this repo)
- Swiss Ephemeris data: installed automatically with `pyswisseph` for typical setups

## Quick start

From the **repository root** (this folder):

```bash
python3.11 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

The app resolves the `astro_sahayogi` package by adding the parent directory of the clone to `sys.path`, so `python main.py` must be run with your current working directory set to the project root (as above).

Alternatively, from the **parent directory** of the clone:

```bash
python -m astro_sahayogi.main
```

## Build for distribution

```bash
python build/nuitka_build.py
```

Installer helpers live under `build/installer/` (macOS DMG script, Windows Inno Setup).

## Architecture

| Area | Role |
|------|------|
| `core/` | Pure computation (no UI imports) |
| `data/` | Constants, translations, color maps |
| `models/` | Dataclass DTOs |
| `services/` | Settings, client DB, exports, licensing |
| `ui/` | PySide6 screens, dialogs, widgets, controllers |
| `build/` | Nuitka config, Inno Setup, create-dmg |
| `graphify-out/` | Knowledge graph artifacts (`GRAPH_REPORT.md`, `graph.json`, `graph.html`) |

## Maintainer

- **GitHub:** [mayankdawar](https://github.com/mayankdawar)
- **Repository:** https://github.com/mayankdawar/astro_sahayogi
- **Contact:** mayankdawar29@gmail.com

## License

Proprietary — All rights reserved.
