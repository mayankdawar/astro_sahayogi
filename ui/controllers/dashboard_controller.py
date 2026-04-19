"""Controller for the dashboard screen: mediates between UI and AstrologyEngine."""
from __future__ import annotations
from datetime import datetime
from typing import Optional

from astro_sahayogi.core.facade import AstrologyEngine
from astro_sahayogi.models.birth_data import BirthData


class DashboardController:
    def __init__(self, engine: AstrologyEngine):
        self._engine = engine
        self._birth_data: Optional[BirthData] = None
        self._mode = "Natal"
        self._rotation = 1
        self._base_time: Optional[datetime] = None
        self._time_offset = 0
        self._transit_base_time: Optional[datetime] = None
        self._transit_offset = 0
        self._horary_base_time: Optional[datetime] = None
        self._horary_offset = 0
        self._last_result: Optional[dict] = None

    def snapshot_mode(self, mode: str) -> dict:
        """Compute chart data for export without mutating last_result."""
        if not self._birth_data or not self._base_time:
            return {}
        return self._engine.process_chart(
            birth_data=self._birth_data,
            mode=mode,
            rotation=self._rotation,
            base_time=self._base_time,
            time_offset_seconds=self._time_offset,
            transit_base_time=self._transit_base_time,
            transit_offset_seconds=self._transit_offset,
            horary_base_time=self._horary_base_time,
            horary_offset_seconds=self._horary_offset,
        )

    def initialize(self, bd: BirthData, base_time: datetime, language: str):
        self._birth_data = bd
        self._base_time = base_time
        self._time_offset = 0
        self._transit_base_time = None
        self._transit_offset = 0
        self._horary_base_time = None
        self._horary_offset = 0
        self._engine.set_language(language)

    def set_mode(self, mode: str):
        self._mode = mode
        if mode == "Transit" and self._transit_base_time is None:
            self._transit_base_time = datetime.now()
        elif mode == "Horary" and self._horary_base_time is None:
            self._horary_base_time = datetime.now()

    def set_rotation(self, rot: int):
        self._rotation = rot

    def adjust_time(self, seconds: int):
        if self._mode == "Natal":
            self._time_offset += seconds
        elif self._mode == "Horary":
            self._horary_offset += seconds
        else:
            self._transit_offset += seconds

    def set_transit_time(self, dt: datetime):
        self._transit_base_time = dt
        self._transit_offset = 0

    def set_horary_time(self, dt: datetime):
        self._horary_base_time = dt
        self._horary_offset = 0

    def compute(self) -> dict:
        if not self._birth_data or not self._base_time:
            return {}

        result = self._engine.process_chart(
            birth_data=self._birth_data,
            mode=self._mode,
            rotation=self._rotation,
            base_time=self._base_time,
            time_offset_seconds=self._time_offset,
            transit_base_time=self._transit_base_time,
            transit_offset_seconds=self._transit_offset,
            horary_base_time=self._horary_base_time,
            horary_offset_seconds=self._horary_offset,
        )
        self._last_result = result
        return result

    def compute_rp(self) -> dict:
        if not self._birth_data:
            return {}
        return self._engine.compute_ruling_planets(
            self._birth_data.timezone,
            self._birth_data.latitude,
            self._birth_data.longitude,
        )

    @property
    def engine(self) -> AstrologyEngine:
        return self._engine

    @property
    def birth_data(self) -> Optional[BirthData]:
        return self._birth_data

    @property
    def mode(self) -> str:
        return self._mode

    @property
    def last_result(self) -> Optional[dict]:
        return self._last_result
