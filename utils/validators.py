"""Input validation helpers."""
from __future__ import annotations


def validate_lat(val: float) -> bool:
    """Check if latitude is within -90 to 90."""
    return -90 <= val <= 90


def validate_lon(val: float) -> bool:
    """Check if longitude is within -180 to 180."""
    return -180 <= val <= 180


def validate_horary(val: int) -> bool:
    """Check if horary number is within 1-249."""
    return 1 <= val <= 249


def validate_age(val: int | str) -> bool:
    """Check if age is within 1-120."""
    try:
        v = int(str(val).strip()) if isinstance(val, str) else val
        return 1 <= v <= 120
    except (ValueError, TypeError):
        return False


def validate_lat_lon(lat_str: str, lon_str: str) -> tuple[float, float] | None:
    """Parse and validate lat/lon from string inputs."""
    try:
        lat = float(lat_str)
        lon = float(lon_str)
        if validate_lat(lat) and validate_lon(lon):
            return lat, lon
    except (ValueError, TypeError):
        pass
    return None


def validate_horary_number(num_str: str) -> int | None:
    """Parse and validate horary number from string."""
    try:
        n = int(num_str)
        if 1 <= n <= 2193:
            return n
    except (ValueError, TypeError):
        pass
    return None
