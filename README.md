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
- **Hardware-fingerprint licensing** (HMAC-based keys; see [Licensing & activation](#licensing--activation))
- **Nuitka** standalone builds (end users do not need Python installed)

---

## Requirements (development)

- **Python 3.11+** (recommended; matches tooling such as Graphify in this repo)
- **PySide6** and other dependencies from `requirements.txt` (Swiss Ephemeris ships with `pyswisseph` for typical installs)

---

## Install and run from source (developers)

Use this when you are working from a Git clone or source tree.

### 1. Clone and enter the project

The repository folder should be named **`astro_sahayogi`** so imports like `astro_sahayogi.app` resolve correctly (the parent directory is added to `sys.path` by `main.py`).

```bash
git clone https://github.com/mayankdawar/astro_sahayogi.git
cd astro_sahayogi
```

### 2. Create a virtual environment (recommended)

```bash
python3.11 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Launch the application

From the **repository root** (the directory that contains `main.py`):

```bash
python main.py
```

Alternatively, from the **parent directory** of the clone (the folder that **contains** the `astro_sahayogi` project folder):

```bash
python -m astro_sahayogi.main
```

**Note:** Always use the **same Python environment** for running the app and for running the Nuitka build (see below). If the build uses Homebrew `python3.11` but you only installed packages in `.venv`, Nuitka will fail with missing **PySide6**.

---

## Distribution: building installers / binaries

This section describes how **you** (the publisher) produce binaries for **end users** who do not install Python.

### What the build produces

The project uses **`build/nuitka_build.py`**, which invokes Nuitka with:

- **`--standalone`** — bundles dependent libraries
- **`--onefile`** — single distributable artifact per platform (plus macOS `.app` bundle layout as configured)
- **`--enable-plugin=pyside6`** — Qt / PySide6 support
- Theme QSS packaged under **`ui/theme`**

After a **successful** build, look under **`dist/`** in the repository root:

| Platform | Typical artifact | How end users run it |
|----------|-------------------|----------------------|
| **macOS** | **`dist/main.app`** (application bundle) | Open `main.app` in Finder (or copy to `/Applications`). First run may require **Right-click → Open** if the app is not notarized. |
| **Windows** | **`dist/main.exe`** | Run `main.exe` (rename to `AstroSahayogi.exe` if you prefer). Windows **SmartScreen** may warn on unsigned binaries. |

Exact filenames follow Nuitka defaults for the entry script **`main.py`**. If you change the entry script name, the output name may change accordingly.

### Prerequisites before you run the build

1. **Same Python as production** — e.g. `python3.11` or an activated **`.venv`** with 3.11.
2. **Install all project dependencies** into that interpreter (Nuitka’s PySide6 plugin imports PySide6 from **this** Python):

   ```bash
   python3.11 -m pip install -r requirements.txt
   ```

3. **Nuitka** is already listed in `requirements.txt`. On **Windows**, you may need the **Visual Studio Build Tools** (MSVC) so Nuitka can compile the C bootstrap; on **macOS**, Xcode Command Line Tools are usually enough.

4. **Optional icons** (recommended for a polished release):
   - **`ui/theme/assets/icon.icns`** — macOS app / Dock icon (otherwise the build uses `--macos-app-icon=none`).
   - **`ui/theme/assets/icon.ico`** — Windows binary and installer icon.

### Run the build

From the repository root:

```bash
python3.11 build/nuitka_build.py
```

The script resolves paths automatically; you can run it from any working directory.

**First build** can take a long time (downloads compiler cache, compiles dependencies). If the build fails, Nuitka may write **`nuitka-crash-report.xml`** in the project root—keep that file when asking for support.

### After the build: packaging for customers

#### macOS — optional DMG

`build/installer/macos_dmg.py` expects:

- A completed build with **`dist/main.app`**
- The **`create-dmg`** tool (e.g. `brew install create-dmg`)

Run from the repository root:

```bash
python3.11 build/installer/macos_dmg.py
```

This creates **`dist/AstroSahayogi.dmg`** (volume name “Astro Sahayogi”). Adjust paths inside the script if Nuitka changes the `.app` name.

**Notarization:** For wide distribution outside the Mac App Store, plan for **Apple notarization** and code signing with an **Apple Developer** account; otherwise Gatekeeper will block or warn users.

#### Windows — optional Inno Setup installer

`build/installer/windows_inno.iss` compiles a setup wizard that:

- Installs **`dist/main.exe`** as **`AstroSahayogi.exe`**
- Creates Start Menu / desktop shortcuts

Steps (on a Windows machine, after Nuitka has produced **`dist/main.exe`**):

1. Install [Inno Setup](https://jrsoftware.org/isinfo.php).
2. Open **`build/installer/windows_inno.iss`** in Inno Setup and compile, **or** use `iscc` from the command line pointing at that script.
3. Output goes to **`dist/installer/`** (see the `[Setup]` section in the `.iss` file).

Uncomment **`SetupIconFile`** in the `.iss` file once **`ui/theme/assets/icon.ico`** exists.

**Code signing:** Signing **`main.exe`** and the installer reduces **SmartScreen** warnings.

---

## Licensing & activation

The codebase includes a **per-machine** licensing mechanism intended for **commercial distribution**:

- **`services/license/fingerprint.py`** — derives a stable **hardware fingerprint** (hash of MAC-derived id, CPU string, OS, architecture).
- **`services/license/keygen.py`** — **seller-side** tool: given a fingerprint, produces an **HMAC-SHA256** license key (uses a **secret** embedded in `keygen.py`; change this secret before any real product launch and **never** ship the secret to customers).
- **`services/license/validator.py`** — loads **`astro_sahayogi_license.json`**, verifies that the stored key matches `generate_license_key(current_fingerprint)`.

### License file format

Create (or let your activation tool create) a file named **`astro_sahayogi_license.json`** next to the working directory from which the user launches the app, with content shaped like:

```json
{
  "license_key": "<hex string from keygen>",
  "fingerprint": "<user machine fingerprint>"
}
```

The validator recomputes the expected key from the **current** machine fingerprint and compares it to **`license_key`**.

**Important:** Today, the license file path is **relative to the process current working directory**, not automatically “next to the .exe”. For a polished product, you may want to resolve the license path relative to the executable (future improvement). Practically: instruct users to **run the app from a folder** that contains **`astro_sahayogi_license.json`**, or set the shortcut “Start in” directory to that folder on Windows.

### How the publisher generates a key (example)

From the **parent directory** of the project folder (so `python -m astro_sahayogi...` resolves):

```bash
cd /path/to/parent_of_repo
python3.11 -m astro_sahayogi.services.license.keygen <PASTE_CUSTOMER_FINGERPRINT_HERE>
```

Alternatively, from **inside** the repo with `PYTHONPATH` pointing at the parent:

```bash
cd /path/to/astro_sahayogi
PYTHONPATH=.. python3.11 -m astro_sahayogi.services.license.keygen <FINGERPRINT>
```

### How to obtain a customer’s fingerprint

From the repo root, with `PYTHONPATH` set so `astro_sahayogi` is importable:

```bash
cd /path/to/astro_sahayogi
PYTHONPATH=.. python3.11 -c "from astro_sahayogi.services.license.fingerprint import get_hardware_fingerprint; print(get_hardware_fingerprint())"
```

Send the printed string to the **publisher**; the publisher runs **keygen** and returns the **license_key** line for the JSON file.

### Startup vs. license check

The splash screen is branded “Initializing…”; **full license enforcement in the UI** is something you can wire to `LicenseValidator.is_licensed()` in `main.py` / splash flow if you want to **require** a valid file before opening the main window. The **validator and keygen** are ready for that workflow.

---

## End-user quick start (binary build)

1. Receive **`main.app`** (macOS) or **`main.exe`** / **`AstroSahayogi_Setup_*.exe`** (Windows installer) from the publisher.
2. **macOS:** If Gatekeeper blocks the app, use **System Settings → Privacy & Security** or **Right-click → Open** the first time.
3. **Windows:** If SmartScreen appears, use “More info → Run anyway” only if you trust the publisher; prefer **signed** builds when possible.
4. If the publisher uses **license files**, place **`astro_sahayogi_license.json`** as instructed and start the app from the agreed working directory (or follow publisher docs).

---

## Architecture (code layout)

| Area | Role |
|------|------|
| `core/` | Pure computation (no UI imports); `AstrologyEngine` in `core/facade.py` is the main API |
| `data/` | Constants, translations, color maps |
| `models/` | Dataclass DTOs |
| `services/` | Settings, client DB, exports, **licensing** |
| `ui/` | PySide6 screens, dialogs, widgets, controllers |
| `build/` | Nuitka entry script, Inno Setup, macOS DMG helper |
| `graphify-out/` | Knowledge graph artifacts (`GRAPH_REPORT.md`, `graph.json`, `graph.html`) |

---

## Maintainer

- **GitHub:** [mayankdawar](https://github.com/mayankdawar)
- **Repository:** https://github.com/mayankdawar/astro_sahayogi
- **Contact:** mayankdawar29@gmail.com

---

## License (legal)

**Proprietary — All rights reserved.**  
Distribution of binaries or source beyond what you are permitted to do in writing is not allowed unless you own the rights or have a license from the copyright holder.
