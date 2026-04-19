"""Formatting utilities: DMS, significator strings."""


def format_dms(longitude: float) -> str:
    """Format longitude-within-sign as degrees/minutes/seconds."""
    d_val = longitude % 30
    deg = int(d_val)
    m = int((d_val - deg) * 60)
    s = int(round((d_val - deg - m / 60) * 3600))
    if s == 60:
        s = 0
        m += 1
    if m == 60:
        m = 0
        deg += 1
    return f"{deg:02d}° {m:02d}' {s:02d}\""


def sig_str(occupation: int, owns: list[int]) -> str:
    """Merge occupation house and owned houses into a sorted comma-separated string."""
    houses = sorted(set([occupation] + owns))
    return ", ".join(map(str, houses))
