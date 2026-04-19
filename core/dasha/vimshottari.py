"""Vimshottari dasha generation and balance calculation."""
from __future__ import annotations
from datetime import datetime, timedelta
from astro_sahayogi.data.constants import LORDS, YRS
from astro_sahayogi.models.dasha_node import DashaNode


def compute_dasha_balance(moon_lon: float, language: str = "English") -> tuple[str, int, float]:
    """Compute dasha balance string and starting lord index.
    
    Returns (balance_str, starting_lord_index, remaining_proportion).
    """
    nak_span = 360.0 / 27.0
    nak_val = moon_lon / nak_span
    idx = int(nak_val) % 9
    rem_prc = 1.0 - (nak_val - int(nak_val))

    bal_y = int(rem_prc * YRS[idx])
    rem_m = (rem_prc * YRS[idx] - bal_y) * 12
    bal_m = int(rem_m)
    bal_d = int((rem_m - bal_m) * 30.436875)

    if language == "Hindi":
        from astro_sahayogi.data.constants import HINDI_PLANETS
        lord_name = HINDI_PLANETS.get(LORDS[idx], LORDS[idx])
        balance_str = f"{lord_name} {bal_y}वर्ष {bal_m}माह {bal_d}दिन"
    else:
        balance_str = f"{LORDS[idx]} {bal_y}Y {bal_m}M {bal_d}D"

    return balance_str, idx, rem_prc


def generate_mahadasha_list(
    moon_lon: float,
    birth_time: datetime,
    highlight_time: datetime,
) -> tuple[list[DashaNode], str]:
    """Generate 9 Mahadasha periods and balance string.
    
    Returns (list of DashaNode, balance_str).
    """
    balance_str, idx, rem_prc = compute_dasha_balance(moon_lon)
    true_start = birth_time - timedelta(days=(1 - rem_prc) * YRS[idx] * 365.2425)
    current_start = true_start
    nodes: list[DashaNode] = []

    for i in range(9):
        d_idx = (idx + i) % 9
        end_date = current_start + timedelta(days=YRS[d_idx] * 365.2425)
        is_active = current_start <= highlight_time <= end_date
        node = DashaNode(
            lord_index=d_idx,
            lord_name=LORDS[d_idx],
            start=current_start,
            end=end_date,
            level=1,
            chain=[d_idx],
            is_active=is_active,
        )
        nodes.append(node)
        current_start = end_date

    return nodes, balance_str


def generate_sub_periods(
    parent_chain: list[int],
    parent_start: datetime,
    parent_level: int,
    highlight_time: datetime | None = None,
    max_level: int = 5,
) -> list[DashaNode]:
    """Generate child dasha periods for a given parent chain.
    
    Works for any level: Antar (2), Pratyantar (3), Sookshma (4), Prana (5).
    """
    level = parent_level + 1
    if level > max_level:
        return []

    parent_lord = parent_chain[-1]
    children: list[DashaNode] = []
    current_start = parent_start

    for i in range(9):
        child_lord = (parent_lord + i) % 9
        new_chain = parent_chain + [child_lord]
        prod = 1.0
        for idx in new_chain:
            prod *= YRS[idx]
        duration_days = (prod / (120 ** (level - 1))) * 365.2425
        end_time = current_start + timedelta(days=duration_days)

        is_active = False
        if highlight_time is not None:
            is_active = current_start <= highlight_time <= end_time

        node = DashaNode(
            lord_index=child_lord,
            lord_name=LORDS[child_lord],
            start=current_start,
            end=end_time,
            level=level,
            chain=new_chain,
            is_active=is_active,
        )
        children.append(node)
        current_start = end_time

    return children


def get_dba_at_time(
    birth_dt: datetime, moon_lon: float, event_dt: datetime,
) -> tuple[str, str, str]:
    """Get Mahadasha-Antardasha-Pratyantardasha lords running at a given event time.
    
    Used by BTR (birth time rectification).
    """
    nak_span = 360.0 / 27.0
    nak_val = moon_lon / nak_span
    idx = int(nak_val) % 9
    rem_prc = 1.0 - (nak_val - int(nak_val))

    md_start = birth_dt - timedelta(days=(1 - rem_prc) * YRS[idx] * 365.2425)
    curr_md = md_start
    md_lord = idx
    for i in range(9):
        d_idx = (idx + i) % 9
        md_end = curr_md + timedelta(days=YRS[d_idx] * 365.2425)
        if curr_md <= event_dt <= md_end:
            md_lord = d_idx
            break
        curr_md = md_end

    curr_ad = curr_md
    ad_lord = md_lord
    for i in range(9):
        a_idx = (md_lord + i) % 9
        ad_days = (YRS[md_lord] * YRS[a_idx]) / 120.0 * 365.2425
        ad_end = curr_ad + timedelta(days=ad_days)
        if curr_ad <= event_dt <= ad_end:
            ad_lord = a_idx
            break
        curr_ad = ad_end

    curr_pd = curr_ad
    pd_lord = ad_lord
    for i in range(9):
        p_idx = (ad_lord + i) % 9
        pd_days = (YRS[md_lord] * YRS[ad_lord] * YRS[p_idx]) / 14400.0 * 365.2425
        pd_end = curr_pd + timedelta(days=pd_days)
        if curr_pd <= event_dt <= pd_end:
            pd_lord = p_idx
            break
        curr_pd = pd_end

    return LORDS[md_lord], LORDS[ad_lord], LORDS[pd_lord]
