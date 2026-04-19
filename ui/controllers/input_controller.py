"""Controller for the input screen: validates data, calls location resolver."""
from __future__ import annotations
from astro_sahayogi.models.birth_data import BirthData
from astro_sahayogi.utils.date_utils import parse_smart_dt
from astro_sahayogi.utils.validators import validate_lat_lon
from astro_sahayogi.core.location.resolver import LocationResolver
from astro_sahayogi.services.settings import SettingsManager
from astro_sahayogi.services.client_repo import ClientRepository
from astro_sahayogi.models.client import Client


class InputController:
    def __init__(self, settings: SettingsManager, client_repo: ClientRepository):
        self._settings = settings
        self._client_repo = client_repo
        self._resolver = LocationResolver()

    def load_settings(self) -> BirthData:
        data = self._settings.load()
        if data:
            return self._settings.to_birth_data()
        return BirthData()

    def save_settings(
        self,
        bd: BirthData,
        language: str,
        ayanamsa: str,
        rahu_pos: str,
        time_format_24h: bool = True,
    ):
        self._settings.from_birth_data(
            bd, language, ayanamsa, rahu_pos, time_format_24h=time_format_24h,
        )

    def validate_and_parse(self, bd: BirthData) -> tuple[bool, str]:
        try:
            parse_smart_dt(bd.datetime_str)
        except ValueError:
            return False, "Invalid date or time format. Use DD-MM-YYYY HH:MM:SS"
        coords = validate_lat_lon(str(bd.latitude), str(bd.longitude))
        if not coords:
            return False, "Invalid latitude/longitude."
        return True, ""

    def fetch_location(self, city: str) -> dict | None:
        return self._resolver.resolve(city)

    def save_client(self, bd: BirthData) -> tuple[bool, str]:
        client = Client(
            name=bd.name, dob=bd.dob, tob=bd.tob, city=bd.city,
            latitude=str(bd.latitude), longitude=str(bd.longitude),
            horary=str(bd.horary_number), timezone=bd.timezone,
        )
        try:
            self._client_repo.save(client)
            return True, f"Chart for '{bd.name}' saved successfully!"
        except ValueError as e:
            return False, str(e)

    def get_all_clients(self) -> list[Client]:
        return self._client_repo.get_all()
