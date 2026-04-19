"""Birth data model."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BirthData:
    name: str = "Happy"
    dob: str = "01-09-1975"
    tob: str = "05:16:00"
    city: str = "Ludhiana"
    latitude: float = 30.9010
    longitude: float = 75.8573
    timezone: str = "Asia/Kolkata"
    horary_number: int = 1
    horary_deg: float = 0.0
    horary_min: float = 0.0
    horary_sec: float = 0.0

    @property
    def datetime_str(self) -> str:
        return f"{self.dob} {self.tob}"

    def to_dict(self) -> dict:
        return {
            "name": self.name, "dob": self.dob, "tob": self.tob,
            "city": self.city, "lat": str(self.latitude), "lon": str(self.longitude),
            "tz": self.timezone, "horary": str(self.horary_number),
        }

    @classmethod
    def from_dict(cls, d: dict) -> BirthData:
        return cls(
            name=d.get("name", "Happy"),
            dob=d.get("dob", "01-09-1975"),
            tob=d.get("tob", "05:16:00"),
            city=d.get("city", "Ludhiana"),
            latitude=float(d.get("lat", 30.9010)),
            longitude=float(d.get("lon", 75.8573)),
            timezone=d.get("tz", "Asia/Kolkata"),
            horary_number=int(d.get("horary", 1)),
        )
