"""Lal Kitab Varshphal (annual chart) calculation."""
from __future__ import annotations
from datetime import datetime, timedelta
import swisseph as swe

from astro_sahayogi.core.lalkitab.matrix import LK_MATRIX
from astro_sahayogi.core.ephemeris.flags import get_swe_flags


def calculate_varshphal(
    birth_time: datetime,
    age: int,
    lat: float,
    lon: float,
    timezone_str: str,
    ayanamsa: str,
    planet_map: dict[str, int],
    tr_p: callable = lambda x: x,
) -> dict:
    """Calculate Lal Kitab Varshphal for a given age.
    
    Returns dict with keys: houses (dict[int, list[str]]), asc_sign, age,
    date_range_str, natal_asc_sign.
    """
    import pytz
    tz = pytz.timezone(timezone_str)
    utc_birth = tz.localize(birth_time).astimezone(pytz.utc)
    jd = swe.julday(utc_birth.year, utc_birth.month, utc_birth.day,
                     utc_birth.hour + utc_birth.minute / 60 + utc_birth.second / 3600)
    flags = get_swe_flags(ayanamsa)

    cusp_orig, _ = swe.houses_ex(jd, lat, lon, b'P', flags=flags)
    true_asc_sign = int(cusp_orig[0] / 30) + 1

    varshphal_houses: dict[int, list[str]] = {i: [] for i in range(1, 13)}

    for p_name, p_id in planet_map.items():
        calc_res = swe.calc_ut(jd, p_id, flags)[0]
        p_lon = calc_res[0]
        p_sign = int(p_lon / 30) + 1
        natal_house = (p_sign - true_asc_sign + 12) % 12 + 1
        v_house = LK_MATRIX[age - 1][natal_house - 1]
        varshphal_houses[v_house].append(tr_p(p_name))

        if p_name == "Rahu":
            ketu_lon = (p_lon + 180.0) % 360.0
            ketu_sign = int(ketu_lon / 30) + 1
            ketu_n_house = (ketu_sign - true_asc_sign + 12) % 12 + 1
            ketu_v_house = LK_MATRIX[age - 1][ketu_n_house - 1]
            varshphal_houses[ketu_v_house].append(tr_p("Ketu"))

    # Date range
    try:
        from_dt = birth_time.replace(year=birth_time.year + age - 1)
    except ValueError:
        from_dt = birth_time + timedelta(days=365.25 * (age - 1))
    try:
        to_dt = birth_time.replace(year=birth_time.year + age)
    except ValueError:
        to_dt = birth_time + timedelta(days=365.25 * age)
    to_dt = to_dt - timedelta(days=1)

    return {
        "houses": varshphal_houses,
        "asc_sign": true_asc_sign,
        "age": age,
        "date_range_str": f"{from_dt.strftime('%d-%m-%Y')} to {to_dt.strftime('%d-%m-%Y')}",
    }
