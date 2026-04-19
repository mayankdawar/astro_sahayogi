"""Tests for input validation utilities."""
import pytest
from astro_sahayogi.utils.validators import validate_lat, validate_lon, validate_horary, validate_age


class TestValidators:
    def test_valid_lat(self):
        assert validate_lat(28.6) is True
        assert validate_lat(-90.0) is True
        assert validate_lat(90.0) is True

    def test_invalid_lat(self):
        assert validate_lat(91.0) is False
        assert validate_lat(-91.0) is False

    def test_valid_lon(self):
        assert validate_lon(77.2) is True
        assert validate_lon(-180.0) is True
        assert validate_lon(180.0) is True

    def test_invalid_lon(self):
        assert validate_lon(181.0) is False
        assert validate_lon(-181.0) is False

    def test_valid_horary(self):
        assert validate_horary(1) is True
        assert validate_horary(249) is True

    def test_invalid_horary(self):
        assert validate_horary(0) is False
        assert validate_horary(250) is False

    def test_valid_age(self):
        assert validate_age(1) is True
        assert validate_age(120) is True

    def test_invalid_age(self):
        assert validate_age(0) is False
        assert validate_age(121) is False
