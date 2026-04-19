"""Birth Time Rectification: RP matching + event verification."""
from __future__ import annotations
from datetime import datetime, timedelta
import pytz
import swisseph as swe

from astro_sahayogi.data.constants import SIGN_LORDS, DAY_LORDS
from astro_sahayogi.core.kp.sublords import get_kp_lords
from astro_sahayogi.core.kp.significators import get_occupation, get_ownership
from astro_sahayogi.core.dasha.vimshottari import get_dba_at_time
from astro_sahayogi.core.ephemeris.flags import get_swe_flags

EVENT_HOUSES = {
    "Marriage (2,7,11)": [2, 7, 11],
    "Childbirth (2,5,11)": [2, 5, 11],
    "Job/Career (2,6,10,11)": [2, 6, 10, 11],
    "Property (4,11,12)": [4, 11, 12],
}


def run_btr(
    approx_dt: datetime,
    range_mins: int,
    step_secs: int,
    events: list[dict],
    timezone_str: str,
    lat: float,
    lon: float,
    ayanamsa: str,
    planet_map: dict[str, int],
    tr_p: callable = lambda x: x,
) -> list[dict]:
    """Run two-stage birth time rectification.
    
    events: list of dicts with keys 'type', 'dt' (datetime).
    Returns list of result dicts for UI display.
    """
    local_tz = pytz.timezone(timezone_str)
    now_dt = datetime.now(local_tz)
    flags = get_swe_flags(ayanamsa)

    jd_now = swe.julday(
        now_dt.astimezone(pytz.utc).year, now_dt.astimezone(pytz.utc).month,
        now_dt.astimezone(pytz.utc).day,
        now_dt.astimezone(pytz.utc).hour + now_dt.astimezone(pytz.utc).minute / 60.0 +
        now_dt.astimezone(pytz.utc).second / 3600.0,
    )

    c_now, _ = swe.houses_ex(jd_now, lat, lon, b'P', flags=flags)
    moon_lon_now = swe.calc_ut(jd_now, swe.MOON, flags)[0][0]
    rp_set = {
        SIGN_LORDS[int(c_now[0] / 30)],
        get_kp_lords(c_now[0])[0],
        SIGN_LORDS[int(moon_lon_now / 30)],
        get_kp_lords(moon_lon_now)[0],
        DAY_LORDS[now_dt.weekday()],
    }

    curr_dt = approx_dt - timedelta(minutes=range_mins)
    end_dt = approx_dt + timedelta(minutes=range_mins)

    blocks = []
    curr_block = None

    while curr_dt <= end_dt:
        utc_b = local_tz.localize(curr_dt).astimezone(pytz.utc)
        jd_b = swe.julday(utc_b.year, utc_b.month, utc_b.day,
                          utc_b.hour + utc_b.minute / 60.0 + utc_b.second / 3600.0)
        asc_lon = swe.houses_ex(jd_b, lat, lon, b'P', flags=flags)[0][0]
        m_lon = swe.calc_ut(jd_b, swe.MOON, flags)[0][0]

        sb = get_kp_lords(asc_lon)[1]
        m_st = get_kp_lords(m_lon)[0]

        key = (sb, m_st)
        if curr_block is None:
            curr_block = {"start": curr_dt, "end": curr_dt, "key": key, "m_lon": m_lon, "jd": jd_b}
        elif curr_block["key"] == key:
            curr_block["end"] = curr_dt
        else:
            blocks.append(curr_block)
            curr_block = {"start": curr_dt, "end": curr_dt, "key": key, "m_lon": m_lon, "jd": jd_b}
        curr_dt += timedelta(seconds=step_secs)

    if curr_block:
        blocks.append(curr_block)

    active_events = []
    for ev in events:
        e_type = ev.get("type", "None")
        if e_type != "None" and ev.get("dt"):
            active_events.append({
                "type": e_type,
                "houses": EVENT_HOUSES.get(e_type, []),
                "dt": ev["dt"],
            })

    results = []
    for b in blocks:
        sb, m_st = b["key"]
        is_rp = sb in rp_set
        is_genetic = sb == m_st

        if is_rp and is_genetic:
            rp_status = "Strong"
        elif is_rp:
            rp_status = "Good"
        else:
            rp_status = "None"

        if rp_status == "None" and active_events:
            continue

        evt_score = 0
        dba_sup_text = []

        if active_events:
            sigs = _get_headless_sigs(b["jd"], lat, lon, flags, planet_map)
            for ev in active_events:
                md, ad, pd = get_dba_at_time(b["start"], b["m_lon"], ev["dt"])
                md_match = bool(set(sigs.get(md, [])) & set(ev["houses"]))
                ad_match = bool(set(sigs.get(ad, [])) & set(ev["houses"]))
                pd_match = bool(set(sigs.get(pd, [])) & set(ev["houses"]))
                if md_match or ad_match or pd_match:
                    evt_score += 1
                dba_sup_text.append(f"[{ev['type'][:4]}: {md[:2]}-{ad[:2]}-{pd[:2]}]")

        if active_events:
            if rp_status == "Strong" and evt_score == len(active_events):
                tag = "strong"
            elif rp_status in ("Strong", "Good") and evt_score >= len(active_events) / 2:
                tag = "good"
            else:
                tag = "normal"
        else:
            tag = "good" if rp_status in ("Strong", "Good") else "normal"

        results.append({
            "time_span": f"{b['start'].strftime('%H:%M:%S')} - {b['end'].strftime('%H:%M:%S')}",
            "asc_sl": tr_p(get_kp_lords(swe.houses_ex(b["jd"], lat, lon, b'P', flags=flags)[0][0])[0]),
            "moon_sl": tr_p(sb),
            "rp_match": rp_status,
            "event_score": f"{evt_score}/{len(active_events)}" if active_events else "N/A",
            "dba_support": ", ".join(dba_sup_text),
            "tag": tag,
        })

    return results


def _get_headless_sigs(jd, lat, lon, flags, planet_map):
    """Quick significator computation without full Nadi logic (for BTR speed)."""
    cusps, _ = swe.houses_ex(jd, lat, lon, b'P', flags=flags)
    chalit_signs = [int(c / 30) + 1 for c in cusps]

    p_data = {}
    for n, p_id in planet_map.items():
        p_lon = swe.calc_ut(jd, p_id, flags)[0][0]
        st, _, _ = get_kp_lords(p_lon)
        p_data[n] = {"lon": p_lon, "st": st}
        if n == "Rahu":
            ketu_lon = (p_lon + 180) % 360
            p_data["Ketu"] = {"lon": ketu_lon, "st": get_kp_lords(ketu_lon)[0]}

    sigs = {}
    for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        if p_name not in p_data:
            continue
        p_lon = p_data[p_name]["lon"]
        occ = get_occupation(p_lon, list(cusps))

        if p_name in ("Rahu", "Ketu"):
            sl = SIGN_LORDS[int(p_lon / 30)]
            owns = [i + 1 for i in range(12) if SIGN_LORDS[chalit_signs[i] - 1] == sl]
        elif p_name not in ("Rahu", "Ketu"):
            owns = [i + 1 for i in range(12) if SIGN_LORDS[chalit_signs[i] - 1] == p_name]
        else:
            owns = []

        st = p_data[p_name]["st"]
        st_lon = p_data[st]["lon"]
        st_occ = get_occupation(st_lon, list(cusps))
        st_owns = [i + 1 for i in range(12) if SIGN_LORDS[chalit_signs[i] - 1] == st]

        sigs[p_name] = list(set([occ] + owns + [st_occ] + st_owns))

    return sigs
