"""Sub-sub lord tracker: detect minute-level changes in planet SSL."""
from __future__ import annotations
from datetime import datetime, timedelta
import pytz
import swisseph as swe

from astro_sahayogi.core.kp.sublords import get_kp_lords
from astro_sahayogi.core.ephemeris.flags import get_swe_flags
from astro_sahayogi.data.constants import ENG_SHORT_ABBR, HINDI_SHORT_ABBR


def run_ssub_tracker(
    from_dt: datetime,
    to_dt: datetime,
    timezone_str: str,
    ayanamsa: str,
    planet_map: dict[str, int],
    language: str = "English",
) -> dict[str, list[dict]]:
    """Track sub-sub lord changes for all planets over a time range.
    
    Returns dict mapping planet_name -> list of {time, new_lords_str}.
    """
    tz = pytz.timezone(timezone_str)
    flags = get_swe_flags(ayanamsa)
    abbr_map = HINDI_SHORT_ABBR if language == "Hindi" else ENG_SHORT_ABBR

    planet_list = ["Moon", "Sun", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

    def get_lon(dt, p_name):
        utc = tz.localize(dt).astimezone(pytz.utc)
        jd = swe.julday(utc.year, utc.month, utc.day,
                        utc.hour + utc.minute / 60 + utc.second / 3600)
        if p_name == "Ketu":
            calc = swe.calc_ut(jd, planet_map.get("Rahu", swe.MEAN_NODE), flags)
            return (calc[0][0] + 180.0) % 360.0
        p_id = planet_map.get(p_name, swe.SUN)
        return swe.calc_ut(jd, p_id, flags)[0][0]

    states = {}
    current_dt = from_dt
    for p in planet_list:
        st, sb, ssb = get_kp_lords(get_lon(current_dt, p))
        states[p] = (st, sb, ssb)

    results: dict[str, list[dict]] = {p: [] for p in planet_list}
    delta_min = timedelta(minutes=1)

    while current_dt < to_dt:
        next_dt = current_dt + delta_min
        for p in planet_list:
            st, sb, ssb = get_kp_lords(get_lon(next_dt, p))
            if (st, sb, ssb) != states[p]:
                for sec in range(1, 61):
                    test_dt = current_dt + timedelta(seconds=sec)
                    t_st, t_sb, t_ssb = get_kp_lords(get_lon(test_dt, p))
                    if (t_st, t_sb, t_ssb) != states[p]:
                        states[p] = (t_st, t_sb, t_ssb)
                        val_str = f"{abbr_map.get(t_st, t_st[:2])}/{abbr_map.get(t_sb, t_sb[:2])}/{abbr_map.get(t_ssb, t_ssb[:2])}"
                        results[p].append({
                            "time": test_dt.strftime("%H:%M:%S"),
                            "lords": val_str,
                        })
                        break
        current_dt = next_dt

    return results
