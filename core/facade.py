"""AstrologyEngine facade: unified API for all astrology computations."""
from __future__ import annotations
from datetime import datetime, timedelta
from typing import Optional
import pytz
import swisseph as swe

from astro_sahayogi.data.constants import (
    PLANETS, SIGN_LORDS, NADI_ORDER, ENG_ABBR, DEFAULT_ORB,
)
from astro_sahayogi.data.translations import I18n
from astro_sahayogi.core.ephemeris.engine import EphemerisEngine
from astro_sahayogi.core.ephemeris.ayanamsa import apply_ayanamsa
from astro_sahayogi.core.ephemeris.flags import get_swe_flags
from astro_sahayogi.core.kp.sublords import get_kp_lords
from astro_sahayogi.core.kp.significators import (
    get_occupation, get_ownership, compute_nadi_significators, compute_full_planet_significators,
)
from astro_sahayogi.core.kp.horary import get_horary_ascendant
from astro_sahayogi.core.kp.ruling_planets import compute_ruling_planets
from astro_sahayogi.core.dasha.vimshottari import generate_mahadasha_list, generate_sub_periods
from astro_sahayogi.core.charts.factory import ChartFactory
from astro_sahayogi.core.analysis.aspects import (
    get_aspect_style, compute_degree_hits_p2p, compute_degree_hits_p2h,
)
from astro_sahayogi.utils.formatting import format_dms, sig_str
from astro_sahayogi.models.birth_data import BirthData


class AstrologyEngine:
    """Single entry point for the UI layer to request any computation.
    
    The UI never imports swisseph or core modules directly.
    """

    def __init__(self):
        self._ephe = EphemerisEngine()
        self._i18n = I18n()
        self._ayanamsa_name = "K.P."
        self._rahu_mode = "Mean"
        self._planet_map = dict(PLANETS)
        self._chart_factory = ChartFactory()

    # ── Configuration ─────────────────────────────────────────────────────

    @property
    def i18n(self) -> I18n:
        return self._i18n

    def set_language(self, lang: str):
        self._i18n.language = lang

    def set_ayanamsa(self, name: str):
        self._ayanamsa_name = name
        apply_ayanamsa(name)

    def set_rahu_mode(self, mode: str):
        self._rahu_mode = mode
        if mode == "TrueNode":
            self._planet_map["Rahu"] = swe.TRUE_NODE
        else:
            self._planet_map["Rahu"] = swe.MEAN_NODE

    def apply_settings(self, ayanamsa: str, rahu_mode: str, language: str):
        self.set_ayanamsa(ayanamsa)
        self.set_rahu_mode(rahu_mode)
        self.set_language(language)

    # ── Flags ─────────────────────────────────────────────────────────────

    def _flags(self, with_speed: bool = False) -> int:
        return get_swe_flags(self._ayanamsa_name, with_speed)

    # ── Core computation ──────────────────────────────────────────────────

    def process_chart(
        self,
        birth_data: BirthData,
        mode: str,
        rotation: int,
        base_time: datetime,
        time_offset_seconds: int = 0,
        transit_base_time: Optional[datetime] = None,
        transit_offset_seconds: int = 0,
        horary_base_time: Optional[datetime] = None,
        horary_offset_seconds: int = 0,
    ) -> dict:
        """Main computation pipeline: houses, planets, significators, dasha, charts.
        
        Returns a comprehensive result dict consumed by the dashboard controller.
        """
        tz = pytz.timezone(birth_data.timezone)
        now_in_tz = datetime.now(tz).replace(tzinfo=None)

        if mode == "Natal":
            cur = base_time + timedelta(seconds=time_offset_seconds)
            highlight_time = now_in_tz
        elif mode == "Horary":
            hb = horary_base_time if horary_base_time is not None else now_in_tz
            cur = hb + timedelta(seconds=horary_offset_seconds)
            highlight_time = cur
        else:
            tb = transit_base_time if transit_base_time is not None else now_in_tz
            cur = tb + timedelta(seconds=transit_offset_seconds)
            highlight_time = cur

        rot = rotation - 1
        utc = tz.localize(cur).astimezone(pytz.utc)
        jd = self._ephe.to_jd(utc.replace(tzinfo=None))
        flags = self._flags()
        flags_speed = self._flags(with_speed=True)
        lat, lon = birth_data.latitude, birth_data.longitude

        cusp_orig, _ = self._ephe.calc_houses(jd, lat, lon, flags)

        if mode == "Horary" and 1 <= birth_data.horary_number <= 2193:
            target_asc = get_horary_ascendant(birth_data.horary_number)
            temp_jd = jd
            for _ in range(15):
                c_temp, _ = self._ephe.calc_houses(temp_jd, lat, lon, flags)
                curr_asc = c_temp[0]
                diff = target_asc - curr_asc
                if diff > 180:
                    diff -= 360
                elif diff < -180:
                    diff += 360
                if abs(diff) < 0.000001:
                    break
                c_plus, _ = self._ephe.calc_houses(temp_jd + 0.0001, lat, lon, flags)
                diff_plus = c_plus[0] - curr_asc
                if diff_plus < 0:
                    diff_plus += 360
                rate = diff_plus / 0.0001
                if rate < 10:
                    rate = 360.0
                temp_jd += diff / rate
            cusp_orig, _ = self._ephe.calc_houses(temp_jd, lat, lon, flags)

        orig_asc_lon = cusp_orig[0]
        orig_asc_sign = int(orig_asc_lon / 30) + 1

        cusp = [cusp_orig[(i + rot) % 12] for i in range(12)]
        asc_sign = int(cusp[0] / 30) + 1
        lagna_signs = [((asc_sign + i - 1) % 12) + 1 for i in range(12)]
        chalit_signs = [int(c / 30) + 1 for c in cusp]

        h_planets_lagna = {i: [] for i in range(1, 13)}
        h_planets_chalit = {i: [] for i in range(1, 13)}

        asc_text = "लग्न" if self._i18n.is_hindi else "Asc"
        l_house_asc = (orig_asc_sign - asc_sign + 12) % 12 + 1
        h_planets_lagna[l_house_asc].append(asc_text)

        for h_idx in range(12):
            h_start, h_end = cusp[h_idx], cusp[(h_idx + 1) % 12]
            if (h_start < h_end and h_start <= orig_asc_lon < h_end) or \
               (h_start > h_end and (orig_asc_lon >= h_start or orig_asc_lon < h_end)):
                h_planets_chalit[h_idx + 1].append(asc_text)
                break

        nak_span = 360.0 / 27.0

        report_cusps = []
        for i in range(12):
            st, sb, ssb = get_kp_lords(cusp[i])
            nak_name = self._i18n.tr_n(int(cusp[i] / nak_span))
            row = (i + 1, self._i18n.tr_z(chalit_signs[i] - 1), format_dms(cusp[i]),
                   nak_name, self._i18n.tr_p(st), self._i18n.tr_p(sb), self._i18n.tr_p(ssb))
            report_cusps.append(row)

        planet_results = self._ephe.get_all_planets(jd, flags, flags_speed, self._planet_map)

        p_data = {}
        report_planets = []
        moon_lon = 0.0

        for idx, pr in enumerate(planet_results):
            p_name = pr["name"]
            p_lon = pr["lon"]
            is_retro = pr["is_retro"]
            st, sb, ssb = get_kp_lords(p_lon)
            nak_name = self._i18n.tr_n(int(p_lon / nak_span))

            p_data[p_name] = {"lon": p_lon, "st": st, "sb": sb, "retro": is_retro}
            if p_name == "Moon":
                moon_lon = p_lon

            disp_name = self._i18n.tr_p(p_name)
            if is_retro:
                disp_name += " (R)" if not self._i18n.is_hindi else " (व)"

            row = (disp_name, self._i18n.tr_z(int(p_lon / 30)), format_dms(p_lon),
                   nak_name, self._i18n.tr_p(st), self._i18n.tr_p(sb), self._i18n.tr_p(ssb))
            report_planets.append(row)

            chart_entry = self._i18n.tr_p(p_name) if self._i18n.is_hindi else ENG_ABBR.get(p_name, p_name[:3])
            if is_retro:
                chart_entry += "(R)" if not self._i18n.is_hindi else "(व)"

            p_sign = int(p_lon / 30) + 1
            l_house = (p_sign - asc_sign + 12) % 12 + 1
            h_planets_lagna[l_house].append(chart_entry)

            for h_idx in range(12):
                h_start, h_end = cusp[h_idx], cusp[(h_idx + 1) % 12]
                if (h_start < h_end and h_start <= p_lon < h_end) or \
                   (h_start > h_end and (p_lon >= h_start or p_lon < h_end)):
                    h_planets_chalit[h_idx + 1].append(chart_entry)
                    break

        nadi_sigs = compute_nadi_significators(p_data, cusp, chalit_signs)
        full_sigs = compute_full_planet_significators(p_data, nadi_sigs)

        report_nadi = []
        planet_significators = {}
        for p in NADI_ORDER:
            if p not in p_data:
                continue
            p_sig = nadi_sigs.get(p, "-")
            st = p_data[p]["st"]
            st_sig = nadi_sigs.get(st, "-")
            sb = p_data[p]["sb"]
            sb_sig = nadi_sigs.get(sb, "-")
            planet_significators[self._i18n.tr_p(p)] = full_sigs.get(p, "")
            report_nadi.append((
                self._i18n.tr_p(p), p_sig,
                self._i18n.tr_p(st), st_sig,
                self._i18n.tr_p(sb), sb_sig,
            ))

        hit_p2p = compute_degree_hits_p2p(p_data, DEFAULT_ORB, self._i18n.tr_p, self._i18n.t)
        hit_p2h = compute_degree_hits_p2h(p_data, cusp, DEFAULT_ORB, self._i18n.tr_p, self._i18n.t, self._i18n.language)

        chart_geom = self._chart_factory.create("north_indian")
        lagna_chart = chart_geom.compute(400, 400, h_planets_lagna, lagna_signs)
        chalit_chart = chart_geom.compute(400, 400, h_planets_chalit, chalit_signs)

        dasha_nodes, balance_str = generate_mahadasha_list(moon_lon, cur, highlight_time)

        return {
            "current_time": cur,
            "highlight_time": highlight_time,
            "cusps": cusp,
            "cusp_orig": cusp_orig,
            "lagna_signs": lagna_signs,
            "chalit_signs": chalit_signs,
            "planet_data": p_data,
            "moon_lon": moon_lon,
            "report_planets": report_planets,
            "report_cusps": report_cusps,
            "report_nadi": report_nadi,
            "planet_significators": planet_significators,
            "nadi_sigs": nadi_sigs,
            "hit_data_p2p": hit_p2p,
            "hit_data_p2h": hit_p2h,
            "h_planets_lagna": h_planets_lagna,
            "h_planets_chalit": h_planets_chalit,
            "lagna_chart": lagna_chart,
            "chalit_chart": chalit_chart,
            "dasha_nodes": dasha_nodes,
            "dasha_balance_str": balance_str,
        }

    def compute_ruling_planets(self, tz_str: str, lat: float, lon: float) -> dict:
        return compute_ruling_planets(tz_str, lat, lon, self._ayanamsa_name)

    def get_kp_lords(self, lon: float) -> tuple[str, str, str]:
        return get_kp_lords(lon)

    def get_horary_ascendant(self, number: int) -> float:
        return get_horary_ascendant(number)

    def get_aspect_style(self, lon1: float, lon2: float) -> tuple:
        return get_aspect_style(lon1, lon2)

    def generate_sub_periods(self, chain, start, level, highlight=None):
        return generate_sub_periods(chain, start, level, highlight)

    @property
    def planet_map(self):
        return self._planet_map

    @property
    def ayanamsa_name(self):
        return self._ayanamsa_name
