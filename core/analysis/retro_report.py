"""Retrograde/direct report: detect speed sign changes over a date range."""
from __future__ import annotations
from datetime import datetime, timedelta
import swisseph as swe

from astro_sahayogi.core.ephemeris.flags import get_swe_flags


def generate_retro_report(
    planet_name: str,
    planet_map: dict[str, int],
    from_date_str: str,
    to_date_str: str,
    ayanamsa: str,
) -> list[dict]:
    """Scan for retrograde/direct transitions."""
    start = datetime.strptime(from_date_str, "%d-%m-%Y")
    end = datetime.strptime(to_date_str, "%d-%m-%Y")
    p_id = planet_map.get(planet_name)
    if p_id is None:
        return []

    flags = get_swe_flags(ayanamsa, with_speed=True)
    results = []
    curr = start
    prev_speed = None

    while curr <= end:
        jd = swe.julday(curr.year, curr.month, curr.day, 12)
        speed = swe.calc_ut(jd, p_id, flags)[0][3]

        if prev_speed is not None:
            if prev_speed > 0 and speed < 0:
                results.append({"date": curr.strftime("%d-%b-%Y"), "status": "Direct -> RETROGRADE"})
            elif prev_speed < 0 and speed > 0:
                results.append({"date": curr.strftime("%d-%b-%Y"), "status": "Retro -> DIRECT"})

        prev_speed = speed
        curr += timedelta(days=1)

    return results
