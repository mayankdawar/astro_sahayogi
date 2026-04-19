"""Tests for horary number ↔ degree mapping."""
import pytest
from astro_sahayogi.core.kp.horary import get_horary_ascendant, get_horary_number


class TestHoraryMapping:
    def test_horary_1_is_zero(self):
        deg = get_horary_ascendant(1)
        assert abs(deg) < 0.01, f"Horary #1 should start near 0°, got {deg}"

    def test_horary_2193_near_360(self):
        deg = get_horary_ascendant(2193)
        assert deg > 350, f"Horary #2193 should be near 360°, got {deg}"

    def test_first_250_monotonic(self):
        prev = -1
        for h in range(1, 251):
            deg = get_horary_ascendant(h)
            assert deg > prev, f"Horary #{h} ({deg}) not > previous ({prev})"
            prev = deg

    def test_round_trip_sample(self):
        for h in [1, 50, 100, 249, 500, 1000, 1500, 2000, 2193]:
            deg = get_horary_ascendant(h)
            back = get_horary_number(deg)
            assert back == h, f"Round trip failed: {h} -> {deg} -> {back}"

    def test_all_in_range(self):
        for h in range(1, 250):
            deg = get_horary_ascendant(h)
            assert 0 <= deg < 360, f"Horary #{h} degree {deg} out of range"

    def test_boundary_values(self):
        for h in [1, 125, 249, 1000, 2193]:
            deg = get_horary_ascendant(h)
            assert isinstance(deg, float)

    def test_invalid_horary_zero(self):
        with pytest.raises(ValueError):
            get_horary_ascendant(0)

    def test_invalid_horary_above_max(self):
        with pytest.raises(ValueError):
            get_horary_ascendant(2194)
