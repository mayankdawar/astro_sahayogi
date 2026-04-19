"""Location resolver: offline geonamescache + online Nominatim fallback."""
from __future__ import annotations
from typing import Optional
import geonamescache
from timezonefinder import TimezoneFinder


class LocationResolver:
    def __init__(self, min_city_population: int = 1000):
        self._gc = geonamescache.GeonamesCache(min_city_population=min_city_population)
        self._tf = TimezoneFinder()

    def resolve(self, city_name: str) -> Optional[dict]:
        """Resolve city to lat/lon/timezone. Returns dict or None.

        Tries exact completer label (City, Region, Country), then offline
        geonamescache by name, then Nominatim.
        """
        from astro_sahayogi.core.location.suggestions import coords_for_suggestion_label

        stripped = city_name.strip()
        hit = coords_for_suggestion_label(stripped)
        if hit:
            tz = hit.get("timezone") or self._tf.timezone_at(
                lng=hit["lon"], lat=hit["lat"]
            ) or "UTC"
            return {"lat": hit["lat"], "lon": hit["lon"], "timezone": tz}

        result = self._resolve_offline(city_name)
        if result:
            return result
        return self._resolve_online(city_name)

    def _resolve_offline(self, city_name: str) -> Optional[dict]:
        matches = self._gc.get_cities_by_name(city_name.strip().title())
        if not matches:
            return None
        city_data_list = []
        for match in matches:
            city_data_list.extend(match.values())
        if not city_data_list:
            return None

        best = sorted(city_data_list, key=lambda x: x.get("population", 0), reverse=True)[0]
        lat, lon = best["latitude"], best["longitude"]
        tz = best.get("timezone") or self._tf.timezone_at(lng=lon, lat=lat) or "UTC"
        return {"lat": lat, "lon": lon, "timezone": tz}

    def _resolve_online(self, city_name: str) -> Optional[dict]:
        try:
            import requests
            url = f"https://nominatim.openstreetmap.org/search?q={city_name.strip()}&format=json&limit=1"
            headers = {"User-Agent": "AstroSahayogi/1.0"}
            response = requests.get(url, headers=headers, timeout=5)
            data = response.json()
            if data:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                tz = self._tf.timezone_at(lng=lon, lat=lat) or "UTC"
                return {"lat": lat, "lon": lon, "timezone": tz}
        except Exception:
            pass
        return None

    def timezone_for(self, lat: float, lon: float) -> str:
        return self._tf.timezone_at(lng=lon, lat=lat) or "UTC"
