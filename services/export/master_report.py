"""Master single-page HTML report exporter."""
from __future__ import annotations
import html as html_lib

from astro_sahayogi.services.export.base import BaseReportExporter


class MasterReportExporter(BaseReportExporter):
    def build_body(self, **kwargs) -> str:
        name = kwargs.get("name", "")
        dob = kwargs.get("dob", "")
        tob = kwargs.get("tob", "")
        city = kwargs.get("city", "")
        mode_display = kwargs.get("mode_display", "Natal")
        rot_display = kwargs.get("rot_display", "1")
        mode_date_info = kwargs.get("mode_date_info", "")
        lagna_svg = kwargs.get("lagna_svg", "")
        chalit_svg = kwargs.get("chalit_svg", "")
        lk_block = kwargs.get("lk_block", "")
        chart_grid_css = kwargs.get("chart_grid_css", "repeat(2, 1fr)")
        planets_html = kwargs.get("planets_html", "")
        cusps_html = kwargs.get("cusps_html", "")
        alt_title = kwargs.get("alt_title", "Transit")
        alt_planets_html = kwargs.get("alt_planets_html", "")
        alt_cusps_html = kwargs.get("alt_cusps_html", "")
        dasha_html = kwargs.get("dasha_html", "")
        balance_str = kwargs.get("balance_str", "")
        running_dasha = kwargs.get("running_dasha", "")
        vastu_html = kwargs.get("vastu_html", "")
        lat = kwargs.get("lat")
        lon = kwargs.get("lon")
        tz = kwargs.get("tz", "")
        horary = kwargs.get("horary")
        t = kwargs.get("t", lambda x: x)

        en = html_lib.escape
        name_e, dob_e, tob_e, city_e = en(str(name)), en(str(dob)), en(str(tob)), en(str(city))
        lat_e = en(str(lat)) if lat is not None else ""
        lon_e = en(str(lon)) if lon is not None else ""
        tz_e = en(str(tz)) if tz else ""
        horary_e = en(str(horary)) if horary is not None else ""
        mode_e = en(str(mode_display))
        rot_e = en(str(rot_display))
        mode_info_e = en(str(mode_date_info))
        balance_e = en(str(balance_str))
        running_e = en(str(running_dasha))
        vastu_body = (
            vastu_html if vastu_html else en(t("Vastu module: use dashboard tools for detailed mapping."))
        )

        meta2 = ""
        if lat is not None and lon is not None:
            meta2 = (
                f"<p><b>{t('Latitude:')}</b> {lat_e} | <b>{t('Longitude:')}</b> {lon_e} "
                f"| <b>{t('Timezone:')}</b> {tz_e}"
            )
            if horary_e:
                meta2 += f" | <b>{t('Horary #:')}</b> {horary_e}"
            meta2 += "</p>"

        return f"""
<div class="header">
  <h1>{t("KP ASTROLOGY MASTER REPORT DETAILS")}</h1>
  <p><b>{t('Name:')}</b> {name_e} | <b>{t('DOB:')}</b> {dob_e} | <b>{t('Time:')}</b> {tob_e} | <b>{t('Place:')}</b> {city_e}</p>
  {meta2}
  <p><b>{t('Mode:')}</b> <span style="color:#e74c3c; font-weight:bold;">{mode_e}</span> | <b>{t('Rotated to House:')}</b> {rot_e}{mode_info_e}</p>
</div>

<div style="display:grid; grid-template-columns:{chart_grid_css}; gap:8px; margin-bottom:8px;">
  <div class="section" style="text-align:center;"><h2>Lagna Chart</h2>{lagna_svg}</div>
  <div class="section" style="text-align:center;"><h2>Bhava Chalit</h2>{chalit_svg}</div>
  {lk_block}
</div>

<div style="display:grid; grid-template-columns:repeat(2,1fr); gap:8px; margin-bottom:8px;">
  <div class="section">
    <h2>{t('Planetary Positions')} ({mode_e})</h2>
    <table><tr><th>{t('Planet')}</th><th>{t('Sign')}</th><th>{t('Degree')}</th><th>{t('Nakshatra')}</th><th>{t('Star Lord')}</th><th>{t('Sub Lord')}</th><th>{t('S-Sub')}</th></tr>{planets_html}</table>
  </div>
  <div class="section">
    <h2>{t('Cusp Positions')} ({mode_e})</h2>
    <table><tr><th>{t('House')}</th><th>{t('Sign')}</th><th>{t('Degree')}</th><th>{t('Nakshatra')}</th><th>{t('Star Lord')}</th><th>{t('Sub Lord')}</th><th>{t('S-Sub')}</th></tr>{cusps_html}</table>
  </div>
  <div class="section">
    <h2>{t('Planetary Positions')} ({en(str(alt_title))})</h2>
    <table><tr><th>{t('Planet')}</th><th>{t('Sign')}</th><th>{t('Degree')}</th><th>{t('Nakshatra')}</th><th>{t('Star Lord')}</th><th>{t('Sub Lord')}</th><th>{t('S-Sub')}</th></tr>{alt_planets_html}</table>
  </div>
  <div class="section">
    <h2>{t('Cusp Positions')} ({en(str(alt_title))})</h2>
    <table><tr><th>{t('House')}</th><th>{t('Sign')}</th><th>{t('Degree')}</th><th>{t('Nakshatra')}</th><th>{t('Star Lord')}</th><th>{t('Sub Lord')}</th><th>{t('S-Sub')}</th></tr>{alt_cusps_html}</table>
  </div>
</div>

<div class="section">
  <h2>{t('Vimshottari Dasha (Current & 3 Levels)')}</h2>
  <div style="padding:5px; font-weight:bold; color:#e74c3c; font-size:10px; text-align:center;">{balance_e}</div>
  <div style="padding:0 5px 5px; font-weight:bold; color:#0d2538; font-size:10px; text-align:center;">{running_e}</div>
  <table><tr><th style="width:40%;">{t('Dasha Lord')}</th><th>{t('Start Date')}</th><th>{t('End Date')}</th></tr>{dasha_html}</table>
</div>

<div class="section" style="margin-top:8px;">
  <h2>{t('Astro Vastu')}</h2>
  <div style="padding:8px; font-size:9px; color:#333;">{vastu_body}</div>
</div>
"""
