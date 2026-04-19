"""Advance multi-planet transit search dialog."""
from __future__ import annotations
from datetime import datetime
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QGroupBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from astro_sahayogi.core.analysis.transit_search import run_transit_search


class TransitSearchDialog(QDialog):
    def __init__(self, timezone_str, ayanamsa, planet_map, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Advance Transit Search Tool")
        self.setMinimumSize(700, 420)
        self._tz = timezone_str
        self._aya = ayanamsa
        self._pmap = planet_map
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Advance Multi-Planet Transit Search")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        top = QHBoxLayout()
        top.addWidget(QLabel("Start From:"))
        self._date = QLineEdit(datetime.now().strftime("%d-%m-%Y"))
        top.addWidget(self._date)
        layout.addLayout(top)

        cond_group = QGroupBox("Set Conditions (Planet to 'None' to ignore)")
        cond_layout = QVBoxLayout(cond_group)
        pl_opts = ["None", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
        star_opts = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
        self._conditions = []
        for i, label in enumerate(["Planet A", "Planet B", "Planet C"]):
            row = QHBoxLayout()
            row.addWidget(QLabel(f"{label}:"))
            p = QComboBox()
            p.addItems(pl_opts)
            row.addWidget(p)
            row.addWidget(QLabel("on Star of"))
            s = QComboBox()
            s.addItems(star_opts)
            row.addWidget(s)
            self._conditions.append((p, s))
            cond_layout.addLayout(row)
        layout.addWidget(cond_group)

        self._result = QLabel("")
        self._result.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self._result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._result)

        btn = QPushButton("Start Search")
        btn.setProperty("accent", True)
        btn.clicked.connect(self._run)
        layout.addWidget(btn)

    def _run(self):
        self._result.setText("Searching...")
        conds = [(p.currentText(), s.currentText()) for p, s in self._conditions if p.currentText() != "None"]
        if not conds:
            self._result.setText("Set at least one condition.")
            return
        result = run_transit_search(conds, self._date.text(), self._tz, self._aya, self._pmap)
        if result:
            self._result.setText(f"Exact Match Found! Date: {result}")
            self._result.setStyleSheet("color: #27AE60;")
        else:
            self._result.setText("No match found within 15 years.")
            self._result.setStyleSheet("color: #E74C3C;")
