"""Dasha tree node model."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class DashaNode:
    lord_index: int                  # index into LORDS
    lord_name: str
    start: datetime
    end: datetime
    level: int                       # 1=Maha, 2=Antar, 3=Pratyantar, 4=Sookshma, 5=Prana
    chain: list[int] = field(default_factory=list)
    is_active: bool = False

    @property
    def duration_days(self) -> float:
        return (self.end - self.start).total_seconds() / 86400.0
