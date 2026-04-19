"""SettingsManager: JSON-based user preferences persistence (Singleton)."""
from __future__ import annotations
import json
import os
from typing import Optional

from astro_sahayogi.models.birth_data import BirthData


class SettingsManager:
    _instance: Optional[SettingsManager] = None
    _DEFAULT_FILE = "kp_user_settings.json"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, filepath: str | None = None):
        if hasattr(self, "_initialized"):
            return
        self._initialized = True
        self._filepath = filepath or self._DEFAULT_FILE
        self._data: dict = {}

    @property
    def filepath(self) -> str:
        return self._filepath

    def load(self) -> dict:
        if os.path.exists(self._filepath):
            try:
                with open(self._filepath, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception as e:
                print(f"Settings load error: {e}")
                self._data = {}
        return self._data

    def save(self, data: dict):
        self._data = data
        try:
            with open(self._filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Settings save error: {e}")

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def to_birth_data(self) -> BirthData:
        return BirthData.from_dict(self._data)

    def from_birth_data(
        self,
        bd: BirthData,
        language: str = "English",
        ayanamsa: str = "K.P.",
        rahu_pos: str = "Mean",
        time_format_24h: bool = True,
    ):
        data = bd.to_dict()
        data["language"] = language
        data["ayanamsa"] = ayanamsa
        data["rahu_pos"] = rahu_pos
        data["time_format_24h"] = time_format_24h
        self.save(data)

    def update_key(self, key: str, value):
        """Merge a single key into persisted settings."""
        self.load()
        self._data[key] = value
        self.save(self._data)
