"""Nadi significator calculations: occupation, ownership, node logic."""
from __future__ import annotations
from astro_sahayogi.data.constants import SIGN_LORDS, ASPECT_RULES, NADI_ORDER
from astro_sahayogi.core.kp.sublords import get_kp_lords


def get_occupation(lon: float, cusps: list[float]) -> int:
    """Return 1-based house number where the planet sits."""
    for i in range(12):
        h_start = cusps[i]
        h_end = cusps[(i + 1) % 12]
        if h_start < h_end:
            if h_start <= lon < h_end:
                return i + 1
        else:
            if lon >= h_start or lon < h_end:
                return i + 1
    return 1


def get_ownership(planet_name: str, chalit_signs: list[int], lon: float) -> list[int]:
    """Return list of 1-based house numbers owned by the planet."""
    effective_name = planet_name
    if planet_name in ("Rahu", "Ketu"):
        effective_name = SIGN_LORDS[int(lon / 30)]

    owns = []
    for i in range(12):
        if SIGN_LORDS[chalit_signs[i] - 1] == effective_name:
            owns.append(i + 1)
    return owns


def compute_nadi_significators(
    planet_data: dict[str, dict],
    cusps: list[float],
    chalit_signs: list[int],
) -> dict[str, str]:
    """Compute full Nadi significators for all planets.
    
    Returns dict mapping planet name -> comma-separated house numbers.
    """
    base_sigs: dict[str, dict] = {}
    for p_name in NADI_ORDER:
        if p_name not in planet_data:
            continue
        lon = planet_data[p_name]["lon"]
        occ = get_occupation(lon, cusps)
        owns = []
        if p_name not in ("Rahu", "Ketu"):
            for i in range(12):
                if SIGN_LORDS[chalit_signs[i] - 1] == p_name:
                    owns.append(i + 1)
        base_sigs[p_name] = {
            "occ": occ,
            "owns": owns,
            "sign_lord": SIGN_LORDS[int(lon / 30)],
        }

    final_sigs: dict[str, str] = {}
    for p_name in NADI_ORDER:
        if p_name not in planet_data:
            continue

        sig_list = [base_sigs[p_name]["occ"]] + base_sigs[p_name]["owns"]

        if p_name in ("Rahu", "Ketu"):
            node_lon = planet_data[p_name]["lon"]
            node_sign = int(node_lon / 30) + 1
            sl = base_sigs[p_name]["sign_lord"]
            if sl in base_sigs:
                sig_list.append(base_sigs[sl]["occ"])
                sig_list.extend(base_sigs[sl]["owns"])

            for other_p, data in base_sigs.items():
                if other_p == p_name or other_p in ("Rahu", "Ketu"):
                    continue
                other_lon = planet_data[other_p]["lon"]
                other_sign = int(other_lon / 30) + 1

                if other_sign == node_sign:
                    sig_list.append(data["occ"])
                    sig_list.extend(data["owns"])

                dist = (node_sign - other_sign + 12) % 12
                if dist == 0:
                    dist = 12
                else:
                    dist += 1

                aspects = ASPECT_RULES.get(other_p, [7])
                if dist in aspects:
                    sig_list.append(data["occ"])
                    sig_list.extend(data["owns"])

        final_sigs[p_name] = ", ".join(map(str, sorted(set(sig_list))))

    return final_sigs


def compute_full_planet_significators(
    planet_data: dict[str, dict],
    nadi_sigs: dict[str, str],
) -> dict[str, str]:
    """Compute combined significators (planet + star lord + sub lord) for each planet."""
    result: dict[str, str] = {}
    for p_name in NADI_ORDER:
        if p_name not in planet_data:
            continue
        p_sig = nadi_sigs.get(p_name, "-")
        st = planet_data[p_name].get("st", "")
        st_sig = nadi_sigs.get(st, "-")
        sb = planet_data[p_name].get("sb", "")
        sb_sig = nadi_sigs.get(sb, "-")

        all_h: list[int] = []
        for sig_s in (p_sig, st_sig, sb_sig):
            if sig_s and sig_s != "-":
                all_h.extend(int(x.strip()) for x in sig_s.split(",") if x.strip().isdigit())

        result[p_name] = ", ".join(map(str, sorted(set(all_h))))
    return result
