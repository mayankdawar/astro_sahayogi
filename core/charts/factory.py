"""Chart factory: create chart geometry instances by type."""
from __future__ import annotations
from astro_sahayogi.core.charts.base import ChartGeometry
from astro_sahayogi.core.charts.north_indian import NorthIndianChart


class ChartFactory:
    _registry: dict[str, type[ChartGeometry]] = {
        "north_indian": NorthIndianChart,
    }

    @classmethod
    def create(cls, chart_type: str = "north_indian") -> ChartGeometry:
        chart_class = cls._registry.get(chart_type, NorthIndianChart)
        return chart_class()

    @classmethod
    def register(cls, name: str, chart_class: type[ChartGeometry]):
        cls._registry[name] = chart_class
