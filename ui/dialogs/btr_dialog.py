"""Auto Birth Time Rectification dialog."""
from __future__ import annotations
from datetime import datetime
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from astro_sahayogi.core.analysis.btr import run_btr, EVENT_HOUSES
from astro_sahayogi.utils.date_utils import parse_smart_dt


class BTRDialog(QDialog):
    def __init__(self, birth_data, timezone_str, lat, lon, ayanamsa, planet_map, i18n, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Auto-BTR (Advanced Two-Stage Rectification)")
        self.setMinimumSize(1000, 650)
        self._bd = birth_data
        self._tz = timezone_str
        self._lat = lat
        self._lon = lon
        self._aya = ayanamsa
        self._pmap = planet_map
        self._i18n = i18n
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("KP Auto-Birth Time Rectification (RP + Event Verification)")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        inp = QGroupBox("Step 1: Base Time Search")
        inp_layout = QHBoxLayout(inp)
        self._date = QLineEdit(self._bd.dob)
        self._time = QLineEdit(self._bd.tob)
        self._range = QLineEdit("15")
        self._step = QLineEdit("10")
        for label, w in [("Date:", self._date), ("Time:", self._time), ("Range (±Mins):", self._range), ("Step (Secs):", self._step)]:
            inp_layout.addWidget(QLabel(label))
            inp_layout.addWidget(w)
        layout.addWidget(inp)

        evt_group = QGroupBox("Step 2: Past Life Events Verification (Optional)")
        evt_layout = QVBoxLayout(evt_group)
        event_types = ["None"] + list(EVENT_HOUSES.keys())
        self._event_combos = []
        self._event_dates = []
        for i in range(3):
            row = QHBoxLayout()
            row.addWidget(QLabel(f"Event {i+1}:"))
            combo = QComboBox()
            combo.addItems(event_types)
            row.addWidget(combo)
            row.addWidget(QLabel("Date:"))
            date_edit = QLineEdit()
            row.addWidget(date_edit)
            self._event_combos.append(combo)
            self._event_dates.append(date_edit)
            evt_layout.addLayout(row)
        layout.addWidget(evt_group)

        self._status = QLabel("Click 'Run Auto-BTR' to start scanning.")
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._status)

        self._table = QTableWidget(0, 6)
        self._table.setHorizontalHeaderLabels(["Time Span", "Asc SL", "Moon SL", "RP Match", "Event Score", "DBA Support"])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self._table)

        btn = QPushButton("Run Auto-BTR")
        btn.setProperty("accent", True)
        btn.clicked.connect(self._run)
        layout.addWidget(btn)

    def _run(self):
        self._table.setRowCount(0)
        self._status.setText("Scanning...")
        try:
            approx_dt = parse_smart_dt(f"{self._date.text()} {self._time.text()}")
        except ValueError:
            self._status.setText("Invalid date/time format.")
            return

        events = []
        for combo, date_edit in zip(self._event_combos, self._event_dates):
            t = combo.currentText()
            d = date_edit.text().strip()
            if t != "None" and d:
                try:
                    events.append({"type": t, "dt": datetime.strptime(d, "%d-%m-%Y")})
                except ValueError:
                    pass

        results = run_btr(approx_dt, int(self._range.text()), int(self._step.text()), events, self._tz, self._lat, self._lon, self._aya, self._pmap, self._i18n.tr_p)

        for r in results:
            row = self._table.rowCount()
            self._table.insertRow(row)
            for c, v in enumerate([r["time_span"], r["asc_sl"], r["moon_sl"], r["rp_match"], r["event_score"], r["dba_support"]]):
                item = QTableWidgetItem(v)
                if r["tag"] == "strong":
                    item.setBackground(QColor("#1E8449"))
                elif r["tag"] == "good":
                    item.setBackground(QColor("#F9E79F"))
                    item.setForeground(QColor("#000000"))
                self._table.setItem(row, c, item)

        self._status.setText(f"Auto-BTR Scan Complete. {len(results)} results found.")
