"""Cusp (house) data model."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class CuspData:
    house_number: int      # 1-12
    longitude: float
    sign_index: int = 0    # 0-based
    nakshatra_index: int = 0
    star_lord: str = ""
    sub_lord: str = ""
    sub_sub_lord: str = ""

    @property
    def sign_number(self) -> int:
        return self.sign_index + 1
