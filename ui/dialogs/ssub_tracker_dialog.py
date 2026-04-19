"""Sub-sub lord tracker matrix dialog."""
from __future__ import annotations
from datetime import datetime, timedelta
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
)
from PySide6.QtGui import QFont
import pytz

from astro_sahayogi.core.analysis.ssub_tracker import run_ssub_tracker
from astro_sahayogi.utils.date_utils import parse_smart_dt


class SSubTrackerDialog(QDialog):
    def __init__(self, timezone_str, ayanamsa, planet_map, language, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Planet Sub-Sub Lord Tracker Matrix")
        self.setMinimumSize(1100, 700)
        self._tz = timezone_str
        self._aya = ayanamsa
        self._pmap = planet_map
        self._lang = language
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        top = QHBoxLayout()
        tz = pytz.timezone(self._tz)
        now = datetime.now(tz)
        self._from = QLineEdit(now.replace(hour=0, minute=0, second=0).strftime("%d-%m-%Y %H:%M:%S"))
        self._to = QLineEdit(now.replace(hour=23, minute=59, second=59).strftime("%d-%m-%Y %H:%M:%S"))
        for label, w in [("From:", self._from), ("To:", self._to)]:
            top.addWidget(QLabel(label))
            top.addWidget(w)
        btn = QPushButton("Generate Matrix")
        btn.setProperty("accent", True)
        btn.clicked.connect(self._run)
        top.addWidget(btn)
        self._status = QLabel("")
        top.addWidget(self._status)
        layout.addLayout(top)

        self._table = QTableWidget()
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self._table)

    def _run(self):
        self._status.setText("Calculating...")
        try:
            dt_from = parse_smart_dt(self._from.text())
            dt_to = parse_smart_dt(self._to.text())
        except ValueError:
            self._status.setText("Invalid format.")
            return
        if (dt_to - dt_from).days > 3:
            self._status.setText("Limit to 3 days max.")
            return

        results = run_ssub_tracker(dt_from, dt_to, self._tz, self._aya, self._pmap, self._lang)

        planet_list = ["Moon", "Sun", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
        max_cols = max((len(results.get(p, [])) for p in planet_list), default=0)
        self._table.setRowCount(len(planet_list))
        self._table.setColumnCount(max_cols + 1)
        self._table.setHorizontalHeaderLabels(["Planet"] + [f"#{i+1}" for i in range(max_cols)])

        for r, p in enumerate(planet_list):
            self._table.setItem(r, 0, QTableWidgetItem(p))
            for c, ev in enumerate(results.get(p, [])):
                self._table.setItem(r, c + 1, QTableWidgetItem(f"{ev['lords']}\n{ev['time']}"))

        self._status.setText(f"Found {sum(len(v) for v in results.values())} changes.")
