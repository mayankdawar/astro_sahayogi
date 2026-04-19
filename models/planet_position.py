"""Planet position model."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class PlanetPosition:
    name: str
    longitude: float
    latitude: float = 0.0
    speed: float = 0.0
    sign_index: int = 0          # 0-based zodiac index
    nakshatra_index: int = 0     # 0-based
    star_lord: str = ""
    sub_lord: str = ""
    sub_sub_lord: str = ""
    is_retrograde: bool = False

    @property
    def sign_number(self) -> int:
        """1-based sign number."""
        return self.sign_index + 1

    @property
    def house_longitude(self) -> float:
        """Longitude within current sign (0-30)."""
        return self.longitude % 30
