"""Abstract base for chart geometry."""
from __future__ import annotations
from abc import ABC, abstractmethod
from astro_sahayogi.models.chart_data import ChartRenderData


class ChartGeometry(ABC):
    @abstractmethod
    def compute(self, width: float, height: float,
                house_data: dict[int, list[str]],
                cusp_signs: list[int] | None = None,
                is_lalkitab: bool = False) -> ChartRenderData: ...
