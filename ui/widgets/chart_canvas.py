"""QGraphicsView-based astrology chart renderer."""
from __future__ import annotations
import html as html_lib
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QSizePolicy
from PySide6.QtGui import QPen, QColor, QFont, QPainter
from PySide6.QtCore import Qt

from astro_sahayogi.models.chart_data import ChartRenderData

DESIGN_SIZE = 400


def chart_render_data_to_svg(data: ChartRenderData | None) -> str:
    """Serialize chart geometry to SVG (for HTML export without a widget)."""
    if not data:
        return ""
    w, h = DESIGN_SIZE, DESIGN_SIZE
    svg = f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">\n'
    svg += f'<rect x="0" y="0" width="{w}" height="{h}" fill="{data.background_color}"/>\n'
    for line in data.lines:
        svg += (
            f'<line x1="{line.x1}" y1="{line.y1}" x2="{line.x2}" y2="{line.y2}" '
            f'stroke="{line.color}" stroke-width="{line.width}"/>\n'
        )
    for txt in data.texts:
        safe = html_lib.escape(txt.text)
        svg += (
            f'<text x="{txt.x}" y="{txt.y + 4}" text-anchor="middle" '
            f'font-size="{txt.font_size}" font-family="Arial" font-weight="{txt.font_weight}" '
            f'fill="{txt.color}">{safe}</text>\n'
        )
    svg += "</svg>"
    return svg


class ChartCanvas(QGraphicsView):
    """Renders a ChartRenderData using Qt's graphics scene with proper scaling."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(300, 300)
        self.setStyleSheet("border: none; background-color: #FDF5E6; border-radius: 6px;")
        self._chart_data: ChartRenderData | None = None

    def set_chart(self, data: ChartRenderData):
        self._chart_data = data
        self._redraw()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._chart_data:
            self._redraw()

    def _redraw(self):
        self._scene.clear()
        if not self._chart_data:
            return

        w = self.viewport().width()
        h = self.viewport().height()
        size = min(w, h)
        if size <= 20:
            return

        self._scene.setSceneRect(0, 0, w, h)
        self._scene.setBackgroundBrush(QColor(self._chart_data.background_color))

        ox = (w - size) / 2
        oy = (h - size) / 2
        scale = size / DESIGN_SIZE

        for line in self._chart_data.lines:
            pen = QPen(QColor(line.color), line.width * scale)
            self._scene.addLine(
                ox + line.x1 * scale,
                oy + line.y1 * scale,
                ox + line.x2 * scale,
                oy + line.y2 * scale,
                pen,
            )

        for txt in self._chart_data.texts:
            font_px = max(9, int(txt.font_size * scale * 1.15))
            font = QFont("Helvetica Neue", font_px)
            if txt.font_weight == "bold":
                font.setWeight(QFont.Weight.Bold)
            item = self._scene.addText(txt.text, font)
            item.setDefaultTextColor(QColor(txt.color))
            item.setPos(
                ox + txt.x * scale - item.boundingRect().width() / 2,
                oy + txt.y * scale - item.boundingRect().height() / 2,
            )

    def to_svg(self) -> str:
        return chart_render_data_to_svg(self._chart_data)
