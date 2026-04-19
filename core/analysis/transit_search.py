"""Advance multi-planet transit search."""
from __future__ import annotations
from datetime import datetime, timedelta
import pytz
import swisseph as swe

from astro_sahayogi.core.kp.sublords import get_kp_lords
from astro_sahayogi.core.ephemeris.flags import get_swe_flags


def run_transit_search(
    conditions: list[tuple[str, str]],
    start_date_str: str,
    timezone_str: str,
    ayanamsa: str,
    planet_map: dict[str, int],
    max_years: int = 15,
) -> str | None:
    """Search for a date when all planet->star conditions are met simultaneously.
    
    conditions: list of (planet_name, target_star_lord).
    Returns date string or None.
    """
    if not conditions:
        return None

    start_dt = datetime.strptime(start_date_str, "%d-%m-%Y").replace(hour=12, minute=0, second=0)
    tz = pytz.timezone(timezone_str)
    flags = get_swe_flags(ayanamsa)

    step_hours = 12
    max_steps = 365 * max_years * 2
    curr_dt = start_dt

    for _ in range(max_steps):
        utc = tz.localize(curr_dt).astimezone(pytz.utc)
        jd = swe.julday(utc.year, utc.month, utc.day,
                        utc.hour + utc.minute / 60.0 + utc.second / 3600.0)

        all_match = True
        for p_name, target_star in conditions:
            if p_name == "Ketu":
                p_id = planet_map.get("Rahu", swe.MEAN_NODE)
                lon = (swe.calc_ut(jd, p_id, flags)[0][0] + 180.0) % 360.0
            else:
                p_id = planet_map.get(p_name, swe.SUN)
                lon = swe.calc_ut(jd, p_id, flags)[0][0]

            st, _, _ = get_kp_lords(lon)
            if st != target_star:
                all_match = False
                break

        if all_match:
            return curr_dt.strftime("%d-%m-%Y")

        curr_dt += timedelta(hours=step_hours)

    return None
