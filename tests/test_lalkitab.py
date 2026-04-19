"""Tests for Lal Kitab matrix and varshphal."""
import pytest
from astro_sahayogi.core.lalkitab.matrix import LK_MATRIX


class TestLKMatrix:
    def test_matrix_dimensions(self):
        assert len(LK_MATRIX) == 120, f"Expected 120 rows, got {len(LK_MATRIX)}"
        for i, row in enumerate(LK_MATRIX):
            assert len(row) == 12, f"Row {i} has {len(row)} columns, expected 12"

    def test_values_in_range(self):
        for i, row in enumerate(LK_MATRIX):
            for j, val in enumerate(row):
                assert 1 <= val <= 12, f"LK_MATRIX[{i}][{j}] = {val} out of [1,12]"

    def test_each_row_uses_all_12_houses(self):
        for i, row in enumerate(LK_MATRIX):
            assert sorted(row) == list(range(1, 13)), f"Row {i} does not contain all houses 1-12: {sorted(row)}"

    def test_first_row(self):
        expected = [1, 9, 10, 3, 5, 2, 11, 7, 6, 12, 4, 8]
        assert LK_MATRIX[0] == expected

    def test_last_row(self):
        expected = [6, 8, 7, 12, 2, 3, 5, 4, 11, 1, 9, 10]
        assert LK_MATRIX[119] == expected
