"""Date and time parsing utilities."""
from datetime import datetime


def parse_smart_dt(dt_str: str) -> datetime:
    """Flexible date/time string parsing (DD-MM-YYYY HH:MM:SS with optional spaces)."""
    clean = dt_str.replace("/", " ").replace("-", " ").replace(":", " ").split()
    if len(clean) >= 5:
        d, m, y, h, mnt = clean[0], clean[1], clean[2], clean[3], clean[4]
        s = clean[5] if len(clean) == 6 else "00"
        return datetime.strptime(
            f"{d:0>2}-{m:0>2}-{y} {h:0>2}:{mnt:0>2}:{s:0>2}",
            "%d-%m-%Y %H:%M:%S",
        )
    return datetime.strptime(dt_str, "%d-%m-%Y %H:%M:%S")
