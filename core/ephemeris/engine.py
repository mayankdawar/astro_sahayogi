"""Swiss Ephemeris wrapper: planet positions, house cusps, Julian day."""
from __future__ import annotations
import swisseph as swe
from datetime import datetime
from typing import Optional

from astro_sahayogi.data.constants import PLANETS, SIGN_LORDS


class EphemerisEngine:
    """Stateless wrapper around pyswisseph for sidereal calculations."""

    def __init__(self):
        swe.set_ephe_path("")

    @staticmethod
    def to_jd(dt: datetime) -> float:
        return swe.julday(dt.year, dt.month, dt.day,
                          dt.hour + dt.minute / 60.0 + dt.second / 3600.0)

    @staticmethod
    def calc_planet(jd: float, planet_id: int, flags: int) -> tuple[float, float, float, float]:
        """Returns (longitude, latitude, distance, speed)."""
        result = swe.calc_ut(jd, planet_id, flags)
        data = result[0]
        return data[0], data[1], data[2], data[3]

    @staticmethod
    def calc_houses(jd: float, lat: float, lon: float, flags: int,
                    house_system: bytes = b'P') -> tuple[list[float], dict]:
        """Returns (12 cusp longitudes, ascmc dict)."""
        cusps, ascmc = swe.houses_ex(jd, lat, lon, house_system, flags=flags)
        return list(cusps), ascmc

    @staticmethod
    def get_all_planets(jd: float, flags: int, flags_speed: int,
                        planet_map: dict[str, int] | None = None
                        ) -> list[dict]:
        """Calculate all planets and return list of dicts with lon, speed, retro status."""
        if planet_map is None:
            planet_map = PLANETS

        results = []
        for name, pid in planet_map.items():
            data = swe.calc_ut(jd, pid, flags_speed)[0]
            lon, speed = data[0], data[3]
            is_retro = False if name in ("Sun", "Moon", "Rahu") else speed < 0
            results.append({
                "name": name, "lon": lon, "speed": speed, "is_retro": is_retro,
            })
            if name == "Rahu":
                results.append({
                    "name": "Ketu", "lon": (lon + 180.0) % 360.0,
                    "speed": 0.0, "is_retro": False,
                })
        return results
