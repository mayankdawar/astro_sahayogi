"""City suggestions from geonamescache: labels with country (and US state), coord lookup."""
from __future__ import annotations
import unicodedata
from functools import lru_cache
from typing import Optional


def _ascii_fold(text: str) -> str:
    """ASCII-friendly form for display/search (e.g. Ludhiāna -> Ludhiana)."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def _format_city_label(info: dict, countries: dict, us_states: dict) -> str:
    raw = (info.get("name") or "").strip()
    name = _ascii_fold(raw) or raw
    cc = (info.get("countrycode") or "").strip()
    a1 = (info.get("admin1code") or "").strip()
    country_name = (countries.get(cc) or {}).get("name") or cc
    if cc == "US" and a1:
        st = us_states.get(a1)
        if st:
            return f"{name}, {st['name']}, {country_name}"
    return f"{name}, {country_name}"


@lru_cache(maxsize=1)
def _city_rows() -> tuple[dict, ...]:
    """Build ordered rows (highest population first) and a flat label->coords map.

    Each row dict: label, lat, lon, timezone, population
    """
    import geonamescache

    gc = geonamescache.GeonamesCache()
    cities = gc.get_cities()
    countries = gc.get_countries()
    us_states = dict(gc.get_us_states())

    by_id: dict[int, dict] = {}
    for _cid, info in cities.items():
        pop = int(info.get("population") or 0)
        if pop < 5000:
            continue
        gid = int(info.get("geonameid") or 0)
        if not gid:
            continue
        label = _format_city_label(info, countries, us_states)
        lat = float(info["latitude"])
        lon = float(info["longitude"])
        tz = info.get("timezone") or ""
        prev = by_id.get(gid)
        if prev is None or pop > prev["population"]:
            by_id[gid] = {
                "label": label,
                "lat": lat,
                "lon": lon,
                "timezone": tz,
                "population": pop,
            }

    ranked = sorted(by_id.values(), key=lambda x: x["population"], reverse=True)
    return tuple(ranked[:12000])


@lru_cache(maxsize=1)
def _label_to_coords() -> dict[str, dict]:
    """Exact display label -> {lat, lon, timezone}. Later rows win on rare dup labels."""
    m: dict[str, dict] = {}
    for row in _city_rows():
        m[row["label"]] = {
            "lat": row["lat"],
            "lon": row["lon"],
            "timezone": row["timezone"],
        }
    return m


def coords_for_suggestion_label(label: str) -> Optional[dict]:
    """Resolve a completer label to lat/lon/timezone, or None."""
    if not label:
        return None
    return _label_to_coords().get(label.strip())


def city_suggestions(query: str, limit: int = 200) -> list[str]:
    """Display strings matching query (substring, case-insensitive)."""
    q = query.strip().lower()
    if len(q) < 1:
        return []
    out: list[str] = []
    for row in _city_rows():
        if q in row["label"].lower():
            out.append(row["label"])
            if len(out) >= limit:
                break
    return out


def all_city_labels_for_completer(max_labels: int = 8000) -> list[str]:
    """Top cities by population for QCompleter."""
    return [row["label"] for row in _city_rows()[:max_labels]]
