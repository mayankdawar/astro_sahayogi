"""Medical astrology dashboard dialog."""
from __future__ import annotations
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QGroupBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from astro_sahayogi.core.analysis.medical import scan_medical_dates, BODY_PARTS, PLANET_DISEASES
from astro_sahayogi.core.kp.sublords import get_kp_lords


class MedicalDialog(QDialog):
    def __init__(self, cusps, planet_data, timezone_str, lat, lon, ayanamsa, i18n, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Medical Astrology & Surgery Timing")
        self.setMinimumSize(900, 600)
        self._cusps = cusps
        self._p_data = planet_data
        self._tz = timezone_str
        self._lat = lat
        self._lon = lon
        self._aya = ayanamsa
        self._i18n = i18n
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("KP Medical Astrology & Health Analysis")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        diag_group = QGroupBox("1. Health Diagnosis (Based on 6, 8, 12 Cusps)")
        diag_layout = QVBoxLayout(diag_group)
        self._diag_table = QTableWidget(0, 6)
        self._diag_table.setHorizontalHeaderLabels(
            ["House", "Signification", "Sub-Lord (CSL)", "Zodiac Sign", "Sensitive Body Part", "Planetary Karaka"])
        self._diag_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._diag_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        diag_layout.addWidget(self._diag_table)
        layout.addWidget(diag_group)
        self._fill_diagnosis()

        timing_group = QGroupBox("2. Treatment / Surgery Favorable Dates (Next 30 Days)")
        timing_layout = QVBoxLayout(timing_group)
        self._timing_table = QTableWidget(0, 5)
        self._timing_table.setHorizontalHeaderLabels(["Date", "Moon Star Lord", "Sub Lord", "Nature of Day", "Recommendation"])
        self._timing_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._timing_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        timing_layout.addWidget(self._timing_table)
        layout.addWidget(timing_group)

        scan_btn = QPushButton("Scan Next 30 Days for Medical Treatment")
        scan_btn.setProperty("accent", True)
        scan_btn.clicked.connect(self._scan)
        layout.addWidget(scan_btn)

    def _fill_diagnosis(self):
        houses = [(6, "Disease / Sickness"), (8, "Surgery / Danger"), (12, "Hospitalization / Defect")]
        for h_num, h_name in houses:
            cusp_deg = self._cusps[h_num - 1]
            _, sb, _ = get_kp_lords(cusp_deg)
            if sb in self._p_data:
                sb_lon = self._p_data[sb]["lon"]
                znum = int(sb_lon / 30) + 1
                body = BODY_PARTS.get(znum, "Unknown")
                zname = self._i18n.tr_z(znum - 1)
            else:
                zname, body = "-", "-"
            karaka = PLANET_DISEASES.get(sb, "-")
            row = self._diag_table.rowCount()
            self._diag_table.insertRow(row)
            for c, v in enumerate([str(h_num), h_name, self._i18n.tr_p(sb), zname, body, karaka]):
                self._diag_table.setItem(row, c, QTableWidgetItem(v))

    def _scan(self):
        self._timing_table.setRowCount(0)
        results = scan_medical_dates(self._cusps, self._tz, self._lat, self._lon, self._aya, 30, self._i18n.tr_p)
        for r in results:
            row = self._timing_table.rowCount()
            self._timing_table.insertRow(row)
            for c, v in enumerate([r["date"], r["moon_star"], r["moon_sub"], r["status"], r["recommendation"]]):
                item = QTableWidgetItem(v)
                if r["tag"] == "safe":
                    item.setBackground(QColor("#1A3A2A"))
                elif r["tag"] == "danger":
                    item.setBackground(QColor("#3A1A1A"))
                self._timing_table.setItem(row, c, item)
