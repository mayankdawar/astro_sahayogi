"""Intraday market predictor using KP sector-wise logic."""
from __future__ import annotations
from datetime import datetime, timedelta
import pytz
import swisseph as swe

from astro_sahayogi.data.constants import SIGN_LORDS
from astro_sahayogi.core.kp.sublords import get_kp_lords
from astro_sahayogi.core.ephemeris.flags import get_swe_flags

SECTOR_PLANETS = {
    "Nifty/Sensex": ["Mercury", "Moon"],
    "Gold (Bullion)": ["Sun", "Mars", "Jupiter"],
    "Silver (Bullion)": ["Moon", "Venus"],
    "IT / Tech Sector": ["Mercury", "Rahu", "Ketu"],
    "Banking & Finance": ["Jupiter", "Mercury"],
    "Metals & Auto": ["Saturn", "Mars"],
    "Pharma & Chemical": ["Rahu", "Ketu", "Sun"],
    "Real Estate": ["Mars", "Saturn"],
}


def scan_intraday(
    cusps: list[float],
    date_str: str,
    open_time: str,
    close_time: str,
    interval_mins: int,
    asset: str,
    timezone_str: str,
    ayanamsa: str,
    tr_p: callable = lambda x: x,
) -> list[dict]:
    """Scan intraday market intervals for bullish/bearish signals."""
    start_dt = datetime.strptime(f"{date_str} {open_time}", "%d-%m-%Y %H:%M")
    end_dt = datetime.strptime(f"{date_str} {close_time}", "%d-%m-%Y %H:%M")

    good_lords = [
        SIGN_LORDS[int(cusps[1] / 30)],
        SIGN_LORDS[int(cusps[4] / 30)],
        SIGN_LORDS[int(cusps[10] / 30)],
    ]
    bad_lords = [
        SIGN_LORDS[int(cusps[5] / 30)],
        SIGN_LORDS[int(cusps[7] / 30)],
        SIGN_LORDS[int(cusps[11] / 30)],
    ]

    active_sector_planets = SECTOR_PLANETS.get(asset, [])
    good_lords.extend(active_sector_planets)

    local_tz = pytz.timezone(timezone_str)
    flags = get_swe_flags(ayanamsa)
    results = []
    curr_dt = start_dt

    while curr_dt <= end_dt:
        utc_dt = local_tz.localize(curr_dt).astimezone(pytz.utc)
        jd_t = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day,
                          utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0)

        m_lon = swe.calc_ut(jd_t, swe.MOON, flags)[0][0]
        m_st, m_sb, m_ssb = get_kp_lords(m_lon)

        score = 0
        active_h = []
        sector_match = "No"

        for lord in (m_st, m_sb, m_ssb):
            if lord in good_lords:
                score += 1
                base_good = [SIGN_LORDS[int(cusps[1] / 30)], SIGN_LORDS[int(cusps[4] / 30)], SIGN_LORDS[int(cusps[10] / 30)]]
                if lord in base_good:
                    active_h.append("2, 5, 11")
            if lord in bad_lords:
                score -= 1
                active_h.append("6, 8, 12")
            if lord in active_sector_planets:
                sector_match = f"Yes ({tr_p(lord)})"
                score += 1

        if score >= 1:
            trend, tag = "Bullish", "bull"
        elif score <= -1:
            trend, tag = "Bearish", "bear"
        else:
            trend, tag = "Wait & Watch", "neutral"

        results.append({
            "time": curr_dt.strftime("%H:%M"),
            "moon_st": tr_p(m_st), "moon_sb": tr_p(m_sb), "moon_ssl": tr_p(m_ssb),
            "active_houses": " / ".join(sorted(set(active_h))) if active_h else "Neutral",
            "sector_match": sector_match, "trend": trend, "tag": tag,
        })
        curr_dt += timedelta(minutes=interval_mins)

    return results
