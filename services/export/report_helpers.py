"""Build HTML fragments for tabular report export."""
from __future__ import annotations
import html as html_lib
from typing import Sequence


def rows_to_table_body(rows: Sequence[Sequence[object]]) -> str:
    lines: list[str] = []
    for row in rows:
        cells = "".join(
            f"<td>{html_lib.escape(str(cell))}</td>" for cell in row
        )
        lines.append(f"<tr>{cells}</tr>")
    return "\n".join(lines)
