"""Tests for license system."""
import pytest
import os
import json
import tempfile
from astro_sahayogi.services.license.fingerprint import get_hardware_fingerprint
from astro_sahayogi.services.license.keygen import generate_license_key
from astro_sahayogi.services.license.validator import LicenseValidator


class TestFingerprint:
    def test_returns_hex_string(self):
        fp = get_hardware_fingerprint()
        assert isinstance(fp, str)
        assert len(fp) == 64  # SHA-256 hex

    def test_deterministic(self):
        a = get_hardware_fingerprint()
        b = get_hardware_fingerprint()
        assert a == b


class TestKeygen:
    def test_generates_key(self):
        key = generate_license_key("test_fingerprint")
        assert isinstance(key, str)
        assert len(key) == 64

    def test_different_fingerprints_different_keys(self):
        k1 = generate_license_key("fp_1")
        k2 = generate_license_key("fp_2")
        assert k1 != k2

    def test_deterministic(self):
        k1 = generate_license_key("same_fp")
        k2 = generate_license_key("same_fp")
        assert k1 == k2


class TestValidator:
    def test_no_file_returns_false(self):
        v = LicenseValidator("/tmp/nonexistent_license_test.json")
        assert v.is_licensed() is False

    def test_activate_and_validate(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            v = LicenseValidator(path)
            fp = v.get_fingerprint()
            key = generate_license_key(fp)
            assert v.activate(key) is True
            assert v.is_licensed() is True
        finally:
            os.unlink(path)

    def test_wrong_key_rejected(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            v = LicenseValidator(path)
            assert v.activate("wrong_key_1234") is False
        finally:
            os.unlink(path)
