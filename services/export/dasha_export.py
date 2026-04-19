"""Dasha HTML table exporter."""
from __future__ import annotations


def dasha_nodes_to_html(nodes: list, max_level: int = 2) -> str:
    """Convert a flat list of dasha nodes to HTML table rows."""
    html = ""
    for node in nodes:
        if node.level > max_level + 1:
            continue
        pad = "&nbsp;" * ((node.level - 1) * 6)
        font_weight = "bold" if node.is_active else "normal"
        bg = " background-color:#d4edda !important;" if node.is_active else ""
        style = f"font-weight:{font_weight};{bg}"
        html += f"<tr><td style='text-align:left; {style}'>{pad}{node.lord_name}</td>"
        html += f"<td style='{style}'>{node.start.strftime('%d-%m-%Y')}</td>"
        html += f"<td style='{style}'>{node.end.strftime('%d-%m-%Y')}</td></tr>"
    return html
