"""Forward check: find when a planet enters a target sign/nakshatra/degree."""
from __future__ import annotations
from datetime import datetime, timedelta
import pytz
import swisseph as swe

from astro_sahayogi.core.ephemeris.flags import get_swe_flags


def run_forward_check(
    planet_name: str,
    planet_map: dict[str, int],
    target_type: str,
    target_value: int | float,
    start_date_str: str,
    timezone_str: str,
    ayanamsa: str,
    max_days: int = 36500,
) -> str | None:
    """Search day-by-day for when a planet enters a target.
    
    Returns date string 'DD-MM-YYYY' or None if not found.
    """
    start_dt = datetime.strptime(start_date_str, "%d-%m-%Y").replace(hour=12, minute=0, second=0)
    p_id = planet_map.get(planet_name, swe.SUN)
    flags = get_swe_flags(ayanamsa)
    tz = pytz.timezone(timezone_str)

    if target_type == "Sign":
        span = 30.0
    elif target_type == "Nakshatra":
        span = 360.0 / 27.0
    else:
        span = 360.0

    curr_dt = start_dt
    prev_in_target = None

    for _ in range(max_days):
        utc = tz.localize(curr_dt).astimezone(pytz.utc)
        jd = swe.julday(utc.year, utc.month, utc.day,
                        utc.hour + utc.minute / 60.0 + utc.second / 3600.0)

        if planet_name == "Ketu":
            r_id = planet_map.get("Rahu", swe.MEAN_NODE)
            lon = (swe.calc_ut(jd, r_id, flags)[0][0] + 180.0) % 360.0
        else:
            lon = swe.calc_ut(jd, p_id, flags)[0][0]

        if target_type in ("Sign", "Nakshatra"):
            curr_idx = int(lon / span)
            is_in_target = curr_idx == int(target_value)
        else:
            target_lon = float(target_value) % 360.0
            diff = abs(lon - target_lon)
            is_in_target = diff < 1.0 or diff > 359.0

        if is_in_target and prev_in_target is False:
            return curr_dt.strftime("%d-%m-%Y")

        prev_in_target = is_in_target if prev_in_target is not None else is_in_target
        curr_dt += timedelta(days=1)

    return None
