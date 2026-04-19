"""Charts-only HTML export."""
from __future__ import annotations
from astro_sahayogi.services.export.base import BaseReportExporter


class ChartsReportExporter(BaseReportExporter):
    def build_body(self, **kwargs) -> str:
        name = kwargs.get("name", "")
        dob = kwargs.get("dob", "")
        tob = kwargs.get("tob", "")
        city = kwargs.get("city", "")
        lagna_svg = kwargs.get("lagna_svg", "")
        chalit_svg = kwargs.get("chalit_svg", "")
        lk_svg = kwargs.get("lk_svg", "")
        lk_title = kwargs.get("lk_title", "Lal Kitab Varshphal")

        return f"""
<div class="header">
  <h1>{name} - Astrological Charts</h1>
  <p><b>DOB:</b> {dob} | <b>Time:</b> {tob} | <b>Place:</b> {city}</p>
</div>
<div style="display:flex; justify-content:center; gap:20px; flex-wrap:wrap;">
  <div class="section" style="text-align:center; padding:10px;">
    <h2>Lagna Chart</h2>{lagna_svg}
  </div>
  <div class="section" style="text-align:center; padding:10px;">
    <h2>Bhava Chalit</h2>{chalit_svg}
  </div>
  <div class="section" style="text-align:center; padding:10px;">
    <h2>{lk_title}</h2>{lk_svg}
  </div>
</div>
"""
