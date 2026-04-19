"""Long-term investment predictor using KP sector-wise logic."""
from __future__ import annotations
from datetime import datetime, timedelta
import pytz
import swisseph as swe

from astro_sahayogi.data.constants import SIGN_LORDS
from astro_sahayogi.core.kp.sublords import get_kp_lords
from astro_sahayogi.core.ephemeris.flags import get_swe_flags

SECTOR_KARAKA_MAP = {
    "Nifty/General Stocks": swe.MERCURY,
    "Gold (Wealth)": swe.JUPITER,
    "Silver": swe.VENUS,
    "Real Estate / Property": swe.SATURN,
    "Banking & Finance": swe.JUPITER,
    "Metals & Auto": swe.MARS,
    "IT / Tech": swe.MERCURY,
    "Pharma": swe.SUN,
}

KARAKA_NAMES = {
    swe.MERCURY: "Mercury", swe.JUPITER: "Jupiter", swe.VENUS: "Venus",
    swe.SATURN: "Saturn", swe.MARS: "Mars", swe.SUN: "Sun",
}


def scan_longterm(
    cusps: list[float],
    from_date_str: str,
    to_date_str: str,
    asset: str,
    step_days: int,
    timezone_str: str,
    ayanamsa: str,
    tr_p: callable = lambda x: x,
) -> list[dict]:
    """Scan long-term investment periods for accumulate/exit signals."""
    start_dt = datetime.strptime(from_date_str, "%d-%m-%Y")
    end_dt = datetime.strptime(to_date_str, "%d-%m-%Y")

    good_lords = [
        SIGN_LORDS[int(cusps[1] / 30)],
        SIGN_LORDS[int(cusps[4] / 30)],
        SIGN_LORDS[int(cusps[10] / 30)],
    ]
    bad_lords = [
        SIGN_LORDS[int(cusps[7] / 30)],
        SIGN_LORDS[int(cusps[11] / 30)],
    ]

    planet_id = SECTOR_KARAKA_MAP.get(asset, swe.JUPITER)
    p_name = KARAKA_NAMES.get(planet_id, "Karaka")

    local_tz = pytz.timezone(timezone_str)
    flags = get_swe_flags(ayanamsa)
    results = []
    curr_dt = start_dt

    while curr_dt <= end_dt:
        utc_dt = local_tz.localize(curr_dt.replace(hour=12, minute=0)).astimezone(pytz.utc)
        jd_t = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour)

        p_lon = swe.calc_ut(jd_t, planet_id, flags)[0][0]
        p_st, p_sb, _ = get_kp_lords(p_lon)

        score = 0
        active_h = []
        for lord in (p_st, p_sb):
            if lord in good_lords:
                score += 1
                active_h.append("2, 5, 11")
            if lord in bad_lords:
                score -= 1
                active_h.append("8, 12")

        if score >= 1:
            trend, tag = "Accumulate (Buy/SIP)", "buy"
        elif score <= -1:
            trend, tag = "Exit (Profit Booking)", "sell"
        else:
            trend, tag = "Hold / Wait", "hold"

        results.append({
            "date": curr_dt.strftime("%d %b %Y"),
            "karaka": p_name,
            "star": tr_p(p_st),
            "sub": tr_p(p_sb),
            "active_houses": " / ".join(sorted(set(active_h))) if active_h else "Neutral",
            "trend": trend, "tag": tag,
        })
        curr_dt += timedelta(days=step_days)

    return results
