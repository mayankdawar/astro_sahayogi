"""Tests for astrological constants integrity."""
import pytest
from astro_sahayogi.data.constants import (
    LORDS, YRS, ZODIAC, NAKSHATRAS, PLANETS, SIGN_LORDS,
    ASPECT_RULES, SIGN_PROPS, HINDI_ZODIAC, HINDI_NAKSHATRAS,
    ENG_ABBR, NADI_ORDER,
)


class TestConstants:
    def test_nine_lords(self):
        assert len(LORDS) == 9

    def test_nine_yrs(self):
        assert len(YRS) == 9

    def test_vimshottari_total(self):
        assert sum(YRS) == 120

    def test_twelve_zodiac(self):
        assert len(ZODIAC) == 12

    def test_twelve_hindi_zodiac(self):
        assert len(HINDI_ZODIAC) == 12

    def test_twentyseven_nakshatras(self):
        assert len(NAKSHATRAS) == 27

    def test_twentyseven_hindi_nakshatras(self):
        assert len(HINDI_NAKSHATRAS) == 27

    def test_planets_count(self):
        assert len(PLANETS) == 8  # Sun through Rahu

    def test_sign_lords_count(self):
        assert len(SIGN_LORDS) == 12

    def test_sign_props_12(self):
        assert len(SIGN_PROPS) == 12
        for i in range(1, 13):
            assert i in SIGN_PROPS

    def test_nadi_order_nine(self):
        assert len(NADI_ORDER) == 9

    def test_eng_abbr_has_all_planets(self):
        for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
            assert p in ENG_ABBR
