"""KP sub-lord calculations: star lord, sub lord, sub-sub lord from longitude."""
from astro_sahayogi.data.constants import LORDS, YRS


def _build_kp_table() -> list[tuple[str, str, str, int]]:
    """Build the full 249-entry KP sub-lord table.

    Returns list of (star_lord, sub_lord, sub_sub_lord, span_arcseconds).
    """
    table = []
    for star in range(27):
        sl_idx = star % 9
        for sub in range(9):
            sb_idx = (sl_idx + sub) % 9
            span = YRS[sb_idx] * 400  # arcseconds
            table.append((LORDS[sl_idx], LORDS[sb_idx], LORDS[sb_idx], span))
    return table


def get_kp_lords(lon: float) -> tuple[str, str, str]:
    """Return (star_lord, sub_lord, sub_sub_lord) for a given sidereal longitude.
    
    Uses integer arc-second arithmetic to avoid floating-point drift.
    """
    lon_sec = int(round((lon + 1e-8) * 3600)) % 1296000

    # 1 Nakshatra = 13°20' = 48,000 arc-seconds
    nak_idx = lon_sec // 48000
    star_lord_idx = nak_idx % 9
    st = LORDS[star_lord_idx]

    # Sub lord
    rem_sec = lon_sec % 48000
    curr_sec = 0
    sb_idx = star_lord_idx
    sub_start_sec = 0
    sb = ""

    for _ in range(9):
        span = YRS[sb_idx] * 400
        curr_sec += span
        if rem_sec < curr_sec:
            sb = LORDS[sb_idx]
            sub_start_sec = curr_sec - span
            break
        sb_idx = (sb_idx + 1) % 9

    # Sub-sub lord (multiply by 3 to avoid float division by 3)
    rem_ss_sec = rem_sec - sub_start_sec
    rem_ss_sec_x3 = rem_ss_sec * 3
    curr_ss_sec_x3 = 0
    ssb_idx = sb_idx
    ssb = ""

    for _ in range(9):
        span_ss_x3 = YRS[sb_idx] * YRS[ssb_idx] * 10
        curr_ss_sec_x3 += span_ss_x3
        if rem_ss_sec_x3 < curr_ss_sec_x3:
            ssb = LORDS[ssb_idx]
            break
        ssb_idx = (ssb_idx + 1) % 9

    return st, sb, ssb
