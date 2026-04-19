"""Client record model for database storage."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Client:
    id: Optional[int] = None
    name: str = ""
    dob: str = ""
    tob: str = ""
    city: str = ""
    latitude: str = ""
    longitude: str = ""
    horary: str = "1"
    timezone: str = "Asia/Kolkata"
    created_at: Optional[str] = None

    def to_tuple(self) -> tuple:
        return (
            self.name, self.dob, self.tob, self.city,
            self.latitude, self.longitude, self.horary,
            self.timezone, self.created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
