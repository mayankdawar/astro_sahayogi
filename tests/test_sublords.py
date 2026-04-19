"""Tests for KP sub-lord calculations."""
import pytest
from astro_sahayogi.core.kp.sublords import get_kp_lords, _build_kp_table


class TestKPSublords:
    """Verify sub-lord table and lookups match known KP reference values."""

    def test_table_length(self):
        table = _build_kp_table()
        assert len(table) == 243, "KP table must have 27 stars × 9 subs = 243 divisions"

    def test_table_covers_full_circle(self):
        table = _build_kp_table()
        total_arcsec = sum(entry[3] for entry in table)
        assert total_arcsec == 360 * 3600, f"Total must equal 1,296,000 arcsec, got {total_arcsec}"

    def test_zero_degrees(self):
        star, sub, ssub = get_kp_lords(0.0)
        assert star == "Ketu", f"Star lord at 0° should be Ketu, got {star}"
        assert sub == "Ketu", f"Sub lord at 0° should be Ketu, got {sub}"

    def test_known_degree_aries_10(self):
        star, sub, ssub = get_kp_lords(10.0)
        assert star in ("Ketu", "Venus", "Sun"), f"Star at 10° Aries should be valid, got {star}"

    def test_boundary_360(self):
        star, sub, ssub = get_kp_lords(359.999)
        assert isinstance(star, str)
        assert isinstance(sub, str)
        assert isinstance(ssub, str)

    def test_pisces_end(self):
        star, sub, ssub = get_kp_lords(359.0)
        assert star == "Mercury", f"Star lord at 359° should be Mercury (Revati), got {star}"

    def test_ketu_first_sub(self):
        star, sub, ssub = get_kp_lords(0.5)
        assert star == "Ketu"

    def test_consistency(self):
        """Same input must always return same output."""
        for deg in [0, 45.5, 90.0, 180.0, 270.0, 355.5]:
            a = get_kp_lords(deg)
            b = get_kp_lords(deg)
            assert a == b

    def test_all_lords_appear(self):
        """Every Vimshottari lord must appear as star lord at least once across the zodiac."""
        from astro_sahayogi.data.constants import LORDS
        seen_stars = set()
        for deg_int in range(0, 360):
            st, _, _ = get_kp_lords(float(deg_int))
            seen_stars.add(st)
        for lord in LORDS:
            assert lord in seen_stars, f"{lord} never appears as star lord"
