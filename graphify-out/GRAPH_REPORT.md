# Graph Report - /Users/MayankDawar/astro_sahayogi  (2026-04-20)

## Corpus Check
- 110 files · ~81,076 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 757 nodes · 1295 edges · 54 communities detected
- Extraction: 59% EXTRACTED · 41% INFERRED · 0% AMBIGUOUS · INFERRED: 526 edges (avg confidence: 0.68)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]

## God Nodes (most connected - your core abstractions)
1. `AstroSahayogiApp` - 57 edges
2. `InputScreen` - 36 edges
3. `BirthData` - 36 edges
4. `App orchestrator: screen navigation and top-level wiring.` - 24 edges
5. `DashboardScreen` - 24 edges
6. `AstrologyEngine` - 24 edges
7. `LocationResolver` - 22 edges
8. `RPPanel` - 19 edges
9. `get_kp_lords()` - 19 edges
10. `DashboardController` - 18 edges

## Surprising Connections (you probably didn't know these)
- `Renders a ChartRenderData using Qt's graphics scene with proper scaling.` --uses--> `ChartRenderData`  [INFERRED]
  /Users/MayankDawar/astro_sahayogi/ui/widgets/chart_canvas.py → /Users/MayankDawar/astro_sahayogi/models/chart_data.py
- `Lazy-loading dasha tree that emits dasha_selected with the chain.` --uses--> `DashaNode`  [INFERRED]
  /Users/MayankDawar/astro_sahayogi/ui/widgets/dasha_tree_widget.py → /Users/MayankDawar/astro_sahayogi/models/dasha_node.py
- `AstroSahayogiApp` --uses--> `AstrologyEngine`  [INFERRED]
  /Users/MayankDawar/astro_sahayogi/app.py → /Users/MayankDawar/astro_sahayogi/core/facade.py
- `AstroSahayogiApp` --uses--> `SettingsManager`  [INFERRED]
  /Users/MayankDawar/astro_sahayogi/app.py → /Users/MayankDawar/astro_sahayogi/services/settings.py
- `AstroSahayogiApp` --uses--> `ClientRepository`  [INFERRED]
  /Users/MayankDawar/astro_sahayogi/app.py → /Users/MayankDawar/astro_sahayogi/services/client_repo.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.03
Nodes (44): compute_degree_hits_p2h(), compute_degree_hits_p2p(), get_aspect_style(), Aspect calculations: degree-based aspect styling and hit detection., Return (diff_360, fg_color, font_weight, bg_color) for an aspect between two lon, Compute planet-to-planet degree aspect hits., Compute planet-to-house cusp degree aspect hits., Compute chart data for export without mutating last_result. (+36 more)

### Community 1 - "Community 1"
Cohesion: 0.03
Nodes (28): AstroSahayogiApp, BTRDialog, Auto Birth Time Rectification dialog., DashboardController, DegreeHitsDialog, Degree hits (P2P and P2H) display dialog., ForwardCheckDialog, Forward checking of planet dialog. (+20 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (35): ChartCanvas, Renders a ChartRenderData using Qt's graphics scene with proper scaling., DashaTreeWidget, Lazy-loading dasha tree that emits dasha_selected with the chain., DashboardScreen, Main dashboard screen with charts, tables, dasha, RP, and tabs., Main dashboard: mode bar, charts, data tabs, dasha tree, RP panel, time controls, Main dashboard: mode bar, charts, data tabs, dasha tree, RP panel, time controls (+27 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (22): App orchestrator: screen navigation and top-level wiring., BirthData, from_dict(), InputController, Controller for the input screen: validates data, calls location resolver., InputScreen, Birth data input form screen., Birth data entry form with horary dual-mode, location fetch, and chart loading. (+14 more)

### Community 4 - "Community 4"
Cohesion: 0.05
Nodes (34): ABC, BaseReportExporter, build_body(), ChartGeometry, compute(), Base report exporter: Template Method pattern., Template Method: subclasses override build_body()., BaseReportExporter (+26 more)

### Community 5 - "Community 5"
Cohesion: 0.05
Nodes (33): Forward check: find when a planet enters a target sign/nakshatra/degree., Search day-by-day for when a planet enters a target.          Returns date strin, run_forward_check(), Resolve city to lat/lon/timezone. Returns dict or None.                  Tries o, generate_retro_report(), Retrograde/direct report: detect speed sign changes over a date range., Scan for retrograde/direct transitions., compute_full_planet_significators() (+25 more)

### Community 6 - "Community 6"
Cohesion: 0.07
Nodes (21): _get_headless_sigs(), Birth Time Rectification: RP matching + event verification., Quick significator computation without full Nadi logic (for BTR speed)., Run two-stage birth time rectification.          events: list of dicts with keys, run_btr(), compute_ruling_planets(), Live ruling planets computation., Compute current ruling planets (Lagna sign/star/sub, Moon sign/star/sub, Day lor (+13 more)

### Community 7 - "Community 7"
Cohesion: 0.1
Nodes (13): Client, ClientListScreen, Client database browser screen., Modal dialog for browsing and selecting saved charts., Client record model for database storage., ClientRepository, ClientRepository: SQLite-based client database with search., Insert a client. Returns the new row id. Raises ValueError on duplicate. (+5 more)

### Community 8 - "Community 8"
Cohesion: 0.09
Nodes (19): DashaNode, Dasha tree node model., Vimshottari dasha tree with lazy loading., Set the function to generate child dasha periods., Set the function to generate child dasha periods., Set the function to generate child dasha periods., Tests for Vimshottari Dasha calculations., TestDashaBalance (+11 more)

### Community 9 - "Community 9"
Cohesion: 0.08
Nodes (18): parse_smart_dt(), Date and time parsing utilities., Flexible date/time string parsing (DD-MM-YYYY HH:MM:SS with optional spaces)., Tests for input validation utilities., TestValidators, Input validation helpers., Check if longitude is within -180 to 180., Check if horary number is within 1-249. (+10 more)

### Community 10 - "Community 10"
Cohesion: 0.12
Nodes (12): get_hardware_fingerprint(), Hardware fingerprint: machine-specific SHA-256 hash., Compute a SHA-256 hash of MAC address + CPU identifier + platform., generate_license_key(), License key generator (seller-side tool).  Usage: python -m astro_sahayogi.servi, Generate an HMAC-SHA256 license key from a hardware fingerprint., Tests for license system., TestFingerprint (+4 more)

### Community 11 - "Community 11"
Cohesion: 0.11
Nodes (9): apply_ayanamsa(), AyanamsaStrategy, FaganAyanamsa, KPAyanamsa, KPNewAyanamsa, LahiriAyanamsa, RamanAyanamsa, Ayanamsa strategy: configures Swiss Ephemeris sidereal mode. (+1 more)

### Community 12 - "Community 12"
Cohesion: 0.16
Nodes (9): get_horary_ascendant(), get_horary_number(), get_number_from_dms(), KP horary number <-> ascendant degree mapping (1-2193)., Map a sidereal longitude (degrees) back to its horary number (1-2193)., Map a degree/min/sec position to the matching horary number., Map a horary number (1-2193) to its ascendant longitude in degrees., Tests for horary number ↔ degree mapping. (+1 more)

### Community 13 - "Community 13"
Cohesion: 0.16
Nodes (8): format_dms(), Formatting utilities: DMS, significator strings., Merge occupation house and owned houses into a sorted comma-separated string., Format longitude-within-sign as degrees/minutes/seconds., sig_str(), Tests for formatting utilities., TestFormatDMS, TestSigStr

### Community 14 - "Community 14"
Cohesion: 0.13
Nodes (2): Tests for astrological constants integrity., TestConstants

### Community 15 - "Community 15"
Cohesion: 0.31
Nodes (2): 12-House relative significations (South KP / Cuspal Interlinks) dialog., SouthKPDialog

### Community 16 - "Community 16"
Cohesion: 0.25
Nodes (2): Tests for Lal Kitab matrix and varshphal., TestLKMatrix

### Community 17 - "Community 17"
Cohesion: 0.33
Nodes (1): Controller for the dashboard screen: mediates between UI and AstrologyEngine.

### Community 18 - "Community 18"
Cohesion: 0.4
Nodes (2): PlanetPosition, Planet position model.

### Community 19 - "Community 19"
Cohesion: 0.5
Nodes (2): CuspData, Cusp (house) data model.

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (1): Astro Sahayogi - KP Astrology Professional Suite.

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (1): Cosmic astrology color palette constants.

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (1): Degree hits computation (convenience wrapper around aspects module).

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (1): Lal Kitab 1952 Engine Matrix (120 rows x 12 columns).

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (1): Astrological constants: zodiac signs, nakshatras, planets, sign properties, Vims

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (0): 

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (0): 

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (0): 

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (0): 

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (0): 

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (0): 

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (0): 

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (0): 

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (0): 

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (0): 

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (0): 

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (0): 

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (0): 

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (1): Returns (longitude, latitude, distance, speed).

### Community 39 - "Community 39"
Cohesion: 1.0
Nodes (1): Returns (12 cusp longitudes, ascmc dict).

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (1): Calculate all planets and return list of dicts with lon, speed, retro status.

### Community 41 - "Community 41"
Cohesion: 1.0
Nodes (0): 

### Community 42 - "Community 42"
Cohesion: 1.0
Nodes (0): 

### Community 43 - "Community 43"
Cohesion: 1.0
Nodes (0): 

### Community 44 - "Community 44"
Cohesion: 1.0
Nodes (1): Longitude within current sign (0-30).

### Community 45 - "Community 45"
Cohesion: 1.0
Nodes (0): 

### Community 46 - "Community 46"
Cohesion: 1.0
Nodes (0): 

### Community 47 - "Community 47"
Cohesion: 1.0
Nodes (0): 

### Community 48 - "Community 48"
Cohesion: 1.0
Nodes (0): 

### Community 49 - "Community 49"
Cohesion: 1.0
Nodes (0): 

### Community 50 - "Community 50"
Cohesion: 1.0
Nodes (1): Return (display_label, population) sorted by population descending.

### Community 51 - "Community 51"
Cohesion: 1.0
Nodes (1): Return display strings matching query (substring, case-insensitive).

### Community 52 - "Community 52"
Cohesion: 1.0
Nodes (1): Top cities by population for QCompleter model.

### Community 53 - "Community 53"
Cohesion: 1.0
Nodes (1): Internationalization helper: thread-safe, standalone (no UI dependency).

## Knowledge Gaps
- **132 isolated node(s):** `Astro Sahayogi - KP Astrology Professional Suite.`, `Splash screen with branding and license check.`, `Branded splash shown on startup while license is verified.`, `Cosmic astrology color palette constants.`, `12-House relative significations (South KP / Cuspal Interlinks) dialog.` (+127 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 20`** (2 nodes): `Astro Sahayogi - KP Astrology Professional Suite.`, `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (2 nodes): `Cosmic astrology color palette constants.`, `palette.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (2 nodes): `Degree hits computation (convenience wrapper around aspects module).`, `degree_hits.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (2 nodes): `Lal Kitab 1952 Engine Matrix (120 rows x 12 columns).`, `matrix.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (2 nodes): `Astrological constants: zodiac signs, nakshatras, planets, sign properties, Vims`, `constants.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (1 nodes): `Returns (longitude, latitude, distance, speed).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (1 nodes): `Returns (12 cusp longitudes, ascmc dict).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (1 nodes): `Calculate all planets and return list of dicts with lon, speed, retro status.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 42`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 43`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 44`** (1 nodes): `Longitude within current sign (0-30).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 45`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 47`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 48`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 49`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 50`** (1 nodes): `Return (display_label, population) sorted by population descending.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 51`** (1 nodes): `Return display strings matching query (substring, case-insensitive).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 52`** (1 nodes): `Top cities by population for QCompleter model.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 53`** (1 nodes): `Internationalization helper: thread-safe, standalone (no UI dependency).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AstroSahayogiApp` connect `Community 1` to `Community 0`, `Community 2`, `Community 3`, `Community 4`, `Community 7`, `Community 15`?**
  _High betweenness centrality (0.187) - this node is a cross-community bridge._
- **Why does `AstrologyEngine` connect `Community 0` to `Community 3`, `Community 1`, `Community 11`, `Community 17`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Why does `App orchestrator: screen navigation and top-level wiring.` connect `Community 3` to `Community 0`, `Community 1`, `Community 2`, `Community 4`, `Community 7`, `Community 15`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `AstroSahayogiApp` (e.g. with `AstrologyEngine` and `SettingsManager`) actually correct?**
  _`AstroSahayogiApp` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `InputScreen` (e.g. with `AstroSahayogiApp` and `App orchestrator: screen navigation and top-level wiring.`) actually correct?**
  _`InputScreen` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 34 inferred relationships involving `BirthData` (e.g. with `AstroSahayogiApp` and `App orchestrator: screen navigation and top-level wiring.`) actually correct?**
  _`BirthData` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 23 inferred relationships involving `App orchestrator: screen navigation and top-level wiring.` (e.g. with `AstrologyEngine` and `SettingsManager`) actually correct?**
  _`App orchestrator: screen navigation and top-level wiring.` has 23 INFERRED edges - model-reasoned connections that need verification._