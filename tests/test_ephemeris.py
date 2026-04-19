"""Tests for ephemeris engine wrapper."""
import pytest
from astro_sahayogi.core.ephemeris.engine import EphemerisEngine
from astro_sahayogi.core.ephemeris.ayanamsa import apply_ayanamsa
from astro_sahayogi.core.ephemeris.flags import get_swe_flags
from datetime import datetime


class TestEphemerisEngine:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = EphemerisEngine()
        apply_ayanamsa("K.P.")

    def test_julian_day_known(self):
        """J2000.0 = 1 Jan 2000 12:00 UT => JD 2451545.0"""
        jd = self.engine.to_jd(datetime(2000, 1, 1, 12, 0, 0))
        assert abs(jd - 2451545.0) < 0.001

    def test_julian_day_monotonic(self):
        jd1 = self.engine.to_jd(datetime(2020, 1, 1))
        jd2 = self.engine.to_jd(datetime(2020, 1, 2))
        assert jd2 > jd1

    def test_planet_calc_returns_valid(self):
        import swisseph as swe
        jd = self.engine.to_jd(datetime(2024, 1, 1, 12, 0, 0))
        flags = get_swe_flags("K.P.")
        result = swe.calc_ut(jd, swe.SUN, flags)
        lon = result[0][0]
        assert 0 <= lon < 360

    def test_houses_returns_12_cusps(self):
        jd = self.engine.to_jd(datetime(2024, 1, 1, 12, 0, 0))
        flags = get_swe_flags("K.P.")
        cusps, ascmc = self.engine.calc_houses(jd, 28.6, 77.2, flags)
        assert len(cusps) == 12
        for c in cusps:
            assert 0 <= c < 360

    def test_all_planets_calculation(self):
        jd = self.engine.to_jd(datetime(2024, 6, 15, 12, 0, 0))
        flags = get_swe_flags("K.P.")
        from astro_sahayogi.data.constants import PLANETS
        results = self.engine.get_all_planets(jd, flags, flags, PLANETS)
        assert len(results) >= len(PLANETS)  # includes Ketu derived from Rahu
        names = [r["name"] for r in results]
        for p in PLANETS:
            assert p in names

    def test_kp_ayanamsa_different_from_western(self):
        """KP flags should differ from no-ayanamsa (Western) flags."""
        kp_flags = get_swe_flags("K.P.")
        west_flags = get_swe_flags("Western")
        assert kp_flags != west_flags
