"""12h / 24h display formatting for datetimes."""
from __future__ import annotations
from datetime import datetime


def format_local_time(dt: datetime, use_24_hour: bool) -> str:
    if use_24_hour:
        return dt.strftime("%H:%M:%S")
    return dt.strftime("%I:%M:%S %p").lstrip("0").replace(" 0", " ")


def format_local_datetime(dt: datetime, use_24_hour: bool) -> str:
    if use_24_hour:
        return dt.strftime("%d-%m-%Y %H:%M:%S")
    return dt.strftime("%d-%m-%Y %I:%M:%S %p")
