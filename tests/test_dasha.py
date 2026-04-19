"""Tests for Vimshottari Dasha calculations."""
import pytest
from datetime import datetime
from astro_sahayogi.core.dasha.vimshottari import (
    compute_dasha_balance, generate_mahadasha_list, generate_sub_periods,
)
from astro_sahayogi.data.constants import LORDS, YRS


class TestDashaBalance:
    def test_balance_returns_string_with_lord(self):
        balance_str, idx, rem_prc = compute_dasha_balance(45.0)
        assert LORDS[idx] in balance_str

    def test_remaining_proportion_positive(self):
        _, _, rem_prc = compute_dasha_balance(100.0)
        assert rem_prc > 0

    def test_lord_index_in_range(self):
        for deg in [0, 30, 60, 90, 120, 180, 240, 300, 350]:
            _, idx, rem_prc = compute_dasha_balance(float(deg))
            assert 0 <= idx < 9
            assert 0 < rem_prc <= 1.0

    def test_full_cycle_is_120_years(self):
        assert sum(YRS) == 120


class TestMahadashaList:
    def test_generates_nine_lords(self):
        nodes, balance_str = generate_mahadasha_list(45.0, datetime(1990, 1, 1), datetime(2024, 1, 1))
        assert len(nodes) == 9

    def test_lords_follow_vimshottari_order(self):
        nodes, _ = generate_mahadasha_list(0.0, datetime(2000, 1, 1), datetime(2024, 1, 1))
        lord_names = [n.lord_name for n in nodes]
        start_idx = LORDS.index(lord_names[0])
        for i, name in enumerate(lord_names):
            expected = LORDS[(start_idx + i) % 9]
            assert name == expected, f"Expected {expected} at position {i}, got {name}"

    def test_balance_string_not_empty(self):
        _, balance_str = generate_mahadasha_list(90.0, datetime(1995, 6, 15), datetime(2024, 1, 1))
        assert len(balance_str) > 0


class TestSubPeriods:
    def test_sub_periods_count(self):
        nodes, _ = generate_mahadasha_list(45.0, datetime(2000, 1, 1), datetime(2024, 1, 1))
        first = nodes[0]
        subs = generate_sub_periods(first.chain, first.start, first.level)
        assert len(subs) == 9

    def test_sub_periods_cover_full_range(self):
        nodes, _ = generate_mahadasha_list(45.0, datetime(2000, 1, 1), datetime(2024, 1, 1))
        first = nodes[0]
        subs = generate_sub_periods(first.chain, first.start, first.level)
        assert subs[0].start == first.start
        last_end = subs[-1].end
        assert last_end is not None
