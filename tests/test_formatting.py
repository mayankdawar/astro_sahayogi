"""Tests for formatting utilities."""
import pytest
from astro_sahayogi.utils.formatting import format_dms, sig_str


class TestFormatDMS:
    def test_zero(self):
        result = format_dms(0.0)
        assert "00° 00'" in result

    def test_known_value_within_sign(self):
        result = format_dms(45.5)
        assert "15° 30'" in result

    def test_exact_sign_boundary(self):
        result = format_dms(30.0)
        assert "00° 00'" in result

    def test_returns_string(self):
        assert isinstance(format_dms(123.456), str)


class TestSigStr:
    def test_single_house(self):
        result = sig_str(3, [])
        assert "3" in result

    def test_with_owned(self):
        result = sig_str(1, [5, 9])
        assert "1" in result
        assert "5" in result
        assert "9" in result

    def test_deduplication(self):
        result = sig_str(3, [3, 7])
        assert result.count("3") == 1
