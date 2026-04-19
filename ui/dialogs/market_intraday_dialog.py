"""Intraday market predictor dialog."""
from __future__ import annotations
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from datetime import datetime

from astro_sahayogi.core.analysis.market_intraday import scan_intraday, SECTOR_PLANETS


class IntradayDialog(QDialog):
    def __init__(self, cusps, timezone_str, ayanamsa, i18n, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Intraday Market Predictor")
        self.setMinimumSize(1000, 650)
        self._cusps = cusps
        self._tz = timezone_str
        self._aya = ayanamsa
        self._i18n = i18n
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("KP Intraday Market Predictor (Sector-Wise)")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        inp = QHBoxLayout()
        self._date = QLineEdit(datetime.now().strftime("%d-%m-%Y"))
        self._open = QLineEdit("09:15")
        self._close = QLineEdit("15:30")
        self._asset = QComboBox()
        self._asset.addItems(list(SECTOR_PLANETS.keys()))
        self._interval = QLineEdit("15")
        for label, w in [("Date:", self._date), ("Open:", self._open), ("Close:", self._close), ("Category:", self._asset), ("Interval:", self._interval)]:
            inp.addWidget(QLabel(label))
            inp.addWidget(w)
        layout.addLayout(inp)

        self._table = QTableWidget(0, 7)
        self._table.setHorizontalHeaderLabels(["Time", "Moon ST", "Moon SB", "Moon SSL", "Active Houses", "Sector Match", "Trend"])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self._table)

        btn = QPushButton("Scan Trend")
        btn.setProperty("accent", True)
        btn.clicked.connect(self._scan)
        layout.addWidget(btn)

    def _scan(self):
        self._table.setRowCount(0)
        results = scan_intraday(
            self._cusps, self._date.text(), self._open.text(), self._close.text(),
            int(self._interval.text() or 15), self._asset.currentText(), self._tz, self._aya, self._i18n.tr_p,
        )
        for r in results:
            row = self._table.rowCount()
            self._table.insertRow(row)
            for c, v in enumerate([r["time"], r["moon_st"], r["moon_sb"], r["moon_ssl"], r["active_houses"], r["sector_match"], r["trend"]]):
                item = QTableWidgetItem(v)
                if r["tag"] == "bull":
                    item.setBackground(QColor("#1A3A2A"))
                elif r["tag"] == "bear":
                    item.setBackground(QColor("#3A1A1A"))
                self._table.setItem(row, c, item)
