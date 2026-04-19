"""Aspect calculations: degree-based aspect styling and hit detection."""
from __future__ import annotations
from astro_sahayogi.data.constants import DEGREE_ASPECTS, DEFAULT_ORB
from astro_sahayogi.data.colors import (
    ASPECT_POSITIVE_FG, ASPECT_POSITIVE_BG,
    ASPECT_NEGATIVE_FG, ASPECT_NEGATIVE_BG,
    ASPECT_NEUTRAL_FG,
)


def get_aspect_style(lon1: float, lon2: float, orb: float = DEFAULT_ORB
                     ) -> tuple[float, str, str, str]:
    """Return (diff_360, fg_color, font_weight, bg_color) for an aspect between two longitudes."""
    diff_360 = (lon2 - lon1) % 360
    shortest_diff = diff_360 if diff_360 <= 180 else 360 - diff_360
    is_excluded = (diff_360 >= 360 - orb) or (diff_360 <= orb)
    if not is_excluded:
        if any(abs(shortest_diff - a) <= orb for a in (45, 90, 135, 180)):
            return diff_360, ASPECT_NEGATIVE_FG, "bold", ASPECT_NEGATIVE_BG
        if any(abs(shortest_diff - a) <= orb for a in (30, 60, 120)):
            return diff_360, ASPECT_POSITIVE_FG, "bold", ASPECT_POSITIVE_BG
    return diff_360, ASPECT_NEUTRAL_FG, "normal", "white"


def compute_degree_hits_p2p(
    planet_data: dict[str, dict],
    orb: float = DEFAULT_ORB,
    tr_p: callable = lambda x: x,
    t: callable = lambda x: x,
) -> list[tuple]:
    """Compute planet-to-planet degree aspect hits."""
    hits = []
    names = list(planet_data.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            p1, p2 = names[i], names[j]
            lon1 = planet_data[p1]["lon"]
            lon2 = planet_data[p2]["lon"]
            diff = abs(lon1 - lon2)
            if diff > 180:
                diff = 360 - diff
            for asp_deg, (asp_name, nature) in DEGREE_ASPECTS.items():
                if abs(diff - asp_deg) <= orb:
                    hits.append((
                        tr_p(p1), tr_p(p2), t(asp_name),
                        f"{diff:.2f}°", t(nature),
                    ))
    return hits


def compute_degree_hits_p2h(
    planet_data: dict[str, dict],
    cusps: list[float],
    orb: float = DEFAULT_ORB,
    tr_p: callable = lambda x: x,
    t: callable = lambda x: x,
    language: str = "English",
) -> list[tuple]:
    """Compute planet-to-house cusp degree aspect hits."""
    hits = []
    for p_name, p_info in planet_data.items():
        lon1 = p_info["lon"]
        for h_idx in range(12):
            lon2 = cusps[h_idx]
            diff = abs(lon1 - lon2)
            if diff > 180:
                diff = 360 - diff
            for asp_deg, (asp_name, nature) in DEGREE_ASPECTS.items():
                if abs(diff - asp_deg) <= orb:
                    disp_h = f"भाव {h_idx + 1}" if language == "Hindi" else f"House {h_idx + 1}"
                    hits.append((
                        tr_p(p_name), disp_h, t(asp_name),
                        f"{diff:.2f}°", t(nature),
                    ))
    return hits
