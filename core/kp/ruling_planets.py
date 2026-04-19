"""Live ruling planets computation."""
from __future__ import annotations
from datetime import datetime
import pytz
import swisseph as swe

from astro_sahayogi.data.constants import SIGN_LORDS, DAY_LORDS
from astro_sahayogi.core.kp.sublords import get_kp_lords
from astro_sahayogi.core.ephemeris.flags import get_swe_flags


def compute_ruling_planets(
    timezone_str: str, lat: float, lon: float, ayanamsa: str,
) -> dict:
    """Compute current ruling planets (Lagna sign/star/sub, Moon sign/star/sub, Day lord)."""
    tz = pytz.timezone(timezone_str)
    now_local = datetime.now(tz)
    utc_now = now_local.astimezone(pytz.utc)

    jd = swe.julday(utc_now.year, utc_now.month, utc_now.day,
                     utc_now.hour + utc_now.minute / 60 + utc_now.second / 3600)
    flags = get_swe_flags(ayanamsa)

    cusp, _ = swe.houses_ex(jd, lat, lon, b'P', flags=flags)
    asc_lon = cusp[0]
    asc_st, asc_sb, _ = get_kp_lords(asc_lon)
    asc_sign_lord = SIGN_LORDS[int(asc_lon / 30)]

    moon_lon = swe.calc_ut(jd, swe.MOON, flags)[0][0]
    moon_st, moon_sb, _ = get_kp_lords(moon_lon)
    moon_sign_lord = SIGN_LORDS[int(moon_lon / 30)]

    day_lord = DAY_LORDS[now_local.weekday()]

    return {
        "now_local": now_local,
        "time": now_local.strftime("%H:%M:%S"),
        "lagna": {"sign_lord": asc_sign_lord, "star_lord": asc_st, "sub_lord": asc_sb},
        "moon": {"sign_lord": moon_sign_lord, "star_lord": moon_st, "sub_lord": moon_sb},
        "day_lord": day_lord,
    }
