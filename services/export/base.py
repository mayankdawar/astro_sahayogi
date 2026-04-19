"""Base report exporter: Template Method pattern."""
from __future__ import annotations
from abc import ABC, abstractmethod


class BaseReportExporter(ABC):
    """Template Method: subclasses override build_body()."""

    def export(self, filepath: str, **kwargs) -> str:
        html = self.build_header(**kwargs)
        html += self.build_body(**kwargs)
        html += self.build_footer(**kwargs)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        return filepath

    def build_header(self, **kwargs) -> str:
        name = kwargs.get("name", "")
        return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>{name} - Astro Sahayogi Report</title>
<style>
  @page {{ margin: 10mm; size: A4; }}
  body {{ font-family: 'Verdana', sans-serif; color: #000; margin: 0; padding: 0;
         font-size: 8.5px; line-height: 1.2; background-color: #fdfcf5; }}
  .master-wrapper {{ max-width: 210mm; margin: 0 auto; padding: 5px; }}
  .header {{ text-align: center; border-bottom: 2.5px solid #0d2538;
             padding-bottom: 5px; margin-bottom: 5px; color: #0d2538; }}
  .header h1 {{ margin: 0 0 6px 0; font-size: 16px; text-transform: uppercase; line-height: 1.25; }}
  .header p {{ margin: 4px 0; line-height: 1.45; font-size: 9px; }}
  .section {{ border: 1.5px solid #0d2538; background: #fff; padding: 3px;
              page-break-inside: avoid; border-radius: 4px; margin-bottom: 8px; }}
  h2 {{ margin: 0 -3px 3px -3px; background: #0d2538; color: #fff; padding: 8px 6px;
       font-size: 10px; text-align: center; text-transform: uppercase; border-radius: 3px 3px 0 0;
       line-height: 1.35; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 8.5px; }}
  th, td {{ border: 1px solid #ccc; padding: 5px 3px; text-align: center; vertical-align: middle; }}
  th {{ background-color: #0d2538; color: #fff; font-weight: bold; font-size: 8.5px; line-height: 1.35; }}
  tr:nth-child(even) td {{ background-color: #f8f9f9; }}
  svg {{ width: 100%; height: auto; max-width: 320px; border: 1px solid #ccc; margin-top: 2px; }}
</style></head><body><div class="master-wrapper">
"""

    @abstractmethod
    def build_body(self, **kwargs) -> str: ...

    def build_footer(self, **kwargs) -> str:
        return "</div></body></html>"
