"""North Indian diamond chart geometry and rendering data."""
from __future__ import annotations
from astro_sahayogi.core.charts.base import ChartGeometry
from astro_sahayogi.models.chart_data import ChartRenderData, ChartLine, ChartText
from astro_sahayogi.data.colors import get_planet_color


class NorthIndianChart(ChartGeometry):
    def compute(self, width: float, height: float,
                house_data: dict[int, list[str]],
                cusp_signs: list[int] | None = None,
                is_lalkitab: bool = False) -> ChartRenderData:
        w, h = width, height
        bg_color = "#ffffff" if is_lalkitab else "#fdf0d5"
        grid_c = "#8b0000" if is_lalkitab else "#8c7b65"
        grid_w = 1.8

        pad = 10
        x1, y1, x2, y2 = pad, pad, w - pad, h - pad
        cx, cy = w / 2, h / 2

        lines = []
        for coords in [
            (x1, y1, x2, y1), (x2, y1, x2, y2), (x2, y2, x1, y2), (x1, y2, x1, y1),
            (x1, y1, x2, y2), (x2, y1, x1, y2),
            (cx, y1, x2, cy), (x2, cy, cx, y2), (cx, y2, x1, cy), (x1, cy, cx, y1),
        ]:
            lines.append(ChartLine(*coords, grid_c, grid_w))

        texts = []

        pos_planets = {
            1: (w/2, h/4), 2: (w/4, h/8), 3: (w/8, h/4), 4: (w/4, h/2),
            5: (w/8, 3*h/4), 6: (w/4, 7*h/8), 7: (w/2, 3*h/4), 8: (3*w/4, 7*h/8),
            9: (7*w/8, 3*h/4), 10: (3*w/4, h/2), 11: (7*w/8, h/4), 12: (3*w/4, h/8),
        }

        pos_signs = {
            1: (w/2, h/2 - 35), 2: (w/4, h/4 - 25), 3: (w/4 - 25, h/4),
            4: (w/2 - 35, h/2), 5: (w/4 - 25, 3*h/4), 6: (w/4, 3*h/4 + 25),
            7: (w/2, h/2 + 35), 8: (3*w/4, 3*h/4 + 25), 9: (3*w/4 + 25, 3*h/4),
            10: (w/2 + 35, h/2), 11: (3*w/4 + 25, h/4), 12: (3*w/4, h/4 - 25),
        }

        for i in range(1, 13):
            if is_lalkitab:
                num_text, num_color = str(i), "#c0392b"
            else:
                num_text = str(cusp_signs[i - 1]) if cusp_signs else ""
                num_color = "#1e8449"

            if num_text:
                texts.append(ChartText(
                    pos_signs[i][0], pos_signs[i][1], num_text, num_color,
                    13 if is_lalkitab else 14, "bold",
                ))

            p_list = house_data.get(i, [])
            if p_list:
                px, py = pos_planets[i]
                line_height = 17
                font_sz = 12
                if len(p_list) > 3:
                    font_sz = 11
                    line_height = 15
                if len(p_list) > 5:
                    font_sz = 10
                    line_height = 14

                current_y = py - ((len(p_list) - 1) * line_height / 2)
                font_weight = "normal" if is_lalkitab else "bold"

                for p in p_list:
                    texts.append(ChartText(
                        px, current_y, p, get_planet_color(p), font_sz, font_weight,
                    ))
                    current_y += line_height

        return ChartRenderData(
            background_color=bg_color, lines=lines, texts=texts,
            houses=house_data, signs=cusp_signs or [],
        )
