"""Swiss Ephemeris flag helpers."""
import swisseph as swe


def get_swe_flags(ayanamsa_name: str, with_speed: bool = False) -> int:
    flags = swe.FLG_SPEED if with_speed else 0
    if ayanamsa_name != "Western":
        flags |= swe.FLG_SIDEREAL
    return flags
