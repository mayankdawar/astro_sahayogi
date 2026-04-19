"""Chart rendering data models."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class ChartLine:
    x1: float
    y1: float
    x2: float
    y2: float
    color: str
    width: float


@dataclass
class ChartText:
    x: float
    y: float
    text: str
    color: str
    font_size: int
    font_weight: str


@dataclass
class ChartRenderData:
    background_color: str
    lines: list[ChartLine] = field(default_factory=list)
    texts: list[ChartText] = field(default_factory=list)
    houses: dict[int, list[str]] = field(default_factory=dict)
    signs: list[int] = field(default_factory=list)
