"""Medical astrology: body part mapping and surgery timing scan."""
from __future__ import annotations
from datetime import datetime, timedelta
import pytz
import swisseph as swe

from astro_sahayogi.data.constants import SIGN_LORDS
from astro_sahayogi.core.kp.sublords import get_kp_lords
from astro_sahayogi.core.ephemeris.flags import get_swe_flags

BODY_PARTS = {
    1: "Head, Brain, Face, Upper Jaw",
    2: "Throat, Neck, Vocal Cords, Right Eye",
    3: "Shoulders, Arms, Collar Bone, Lungs",
    4: "Chest, Breast, Heart, Lungs",
    5: "Stomach, Liver, Gall Bladder, Spine",
    6: "Intestines, Kidneys, Lower Abdomen",
    7: "Pelvis, Uterus, Lumbar Region",
    8: "Genitals, Rectum, Prostate",
    9: "Thighs, Hips, Arterial System",
    10: "Knees, Bones, Joints",
    11: "Calves, Ankles, Blood Circulation",
    12: "Feet, Toes, Immune System, Left Eye",
}

PLANET_DISEASES = {
    "Sun": "Heart, Bones, Vitality, Eyes",
    "Moon": "Blood, Fluids, Mind, Chest",
    "Mars": "Surgery, Accidents, Infections, Muscles",
    "Mercury": "Nerves, Skin, Brain",
    "Jupiter": "Liver, Tumors, Diabetes, Fat",
    "Venus": "Kidneys, Reproductive, Throat",
    "Saturn": "Chronic issues, Teeth, Paralysis",
    "Rahu": "Undiagnosed, Phobias, Poisons",
    "Ketu": "Viral, Epidemics, Mysterious ailments",
}


def scan_medical_dates(
    cusps: list[float],
    timezone_str: str,
    lat: float,
    lon: float,
    ayanamsa: str,
    days: int = 30,
    tr_p: callable = lambda x: x,
) -> list[dict]:
    """Scan next N days for medical treatment favorability."""
    lord_5 = SIGN_LORDS[int(cusps[4] / 30)]
    lord_11 = SIGN_LORDS[int(cusps[10] / 30)]
    lord_8 = SIGN_LORDS[int(cusps[7] / 30)]
    lord_12 = SIGN_LORDS[int(cusps[11] / 30)]

    local_tz = pytz.timezone(timezone_str)
    start_dt = datetime.now(local_tz)
    flags = get_swe_flags(ayanamsa)
    results = []

    for day_offset in range(days):
        check_dt = (start_dt + timedelta(days=day_offset)).replace(hour=12, minute=0, second=0)
        utc_dt = check_dt.astimezone(pytz.utc)
        jd_t = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day,
                          utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0)

        m_lon = swe.calc_ut(jd_t, swe.MOON, flags)[0][0]
        m_st, m_sb, _ = get_kp_lords(m_lon)

        if m_st in (lord_5, lord_11):
            status, rec, tag = "Favorable (Cure)", "Safe for Treatment/Surgery.", "safe"
        elif m_st in (lord_8, lord_12):
            status, rec, tag = "Unfavorable (Risk)", "Avoid Major Surgery if possible.", "danger"
        else:
            status, rec, tag = "Neutral", "Routine care.", "neutral"

        results.append({
            "date": check_dt.strftime("%d %b %Y"),
            "moon_star": tr_p(m_st),
            "moon_sub": tr_p(m_sb),
            "status": status,
            "recommendation": rec,
            "tag": tag,
        })
    return results
