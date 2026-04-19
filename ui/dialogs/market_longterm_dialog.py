"""Long-term wealth predictor dialog."""
from __future__ import annotations
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from datetime import datetime, timedelta

from astro_sahayogi.core.analysis.market_longterm import scan_longterm


class LongtermDialog(QDialog):
    def __init__(self, cusps, timezone_str, ayanamsa, i18n, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Long-Term Wealth & Investment Predictor")
        self.setMinimumSize(1000, 650)
        self._cusps = cusps
        self._tz = timezone_str
        self._aya = ayanamsa
        self._i18n = i18n
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("KP Long-Term Positional & SIP Predictor")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        inp = QHBoxLayout()
        self._from = QLineEdit(datetime.now().strftime("%d-%m-%Y"))
        self._to = QLineEdit((datetime.now() + timedelta(days=365)).strftime("%d-%m-%Y"))
        self._asset = QComboBox()
        self._asset.addItems(["Nifty/General Stocks", "Gold (Wealth)", "Silver", "Real Estate / Property", "Banking & Finance", "IT / Tech", "Metals & Auto", "Pharma"])
        self._interval = QComboBox()
        self._interval.addItems(["Daily (1 Day)", "Weekly (7 Days)", "Monthly (30 Days)"])
        self._interval.setCurrentIndex(1)
        for label, w in [("From:", self._from), ("To:", self._to), ("Sector:", self._asset), ("Interval:", self._interval)]:
            inp.addWidget(QLabel(label))
            inp.addWidget(w)
        layout.addLayout(inp)

        self._table = QTableWidget(0, 6)
        self._table.setHorizontalHeaderLabels(["Date", "Karaka Planet", "Planet ST", "Planet SB", "Active Houses", "Phase / Action"])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self._table)

        btn = QPushButton("Scan Long-Term Plan")
        btn.setProperty("accent", True)
        btn.clicked.connect(self._scan)
        layout.addWidget(btn)

    def _scan(self):
        self._table.setRowCount(0)
        int_val = self._interval.currentText()
        step = 1 if "Daily" in int_val else 7 if "Weekly" in int_val else 30
        results = scan_longterm(self._cusps, self._from.text(), self._to.text(), self._asset.currentText(), step, self._tz, self._aya, self._i18n.tr_p)
        for r in results:
            row = self._table.rowCount()
            self._table.insertRow(row)
            for c, v in enumerate([r["date"], r["karaka"], r["star"], r["sub"], r["active_houses"], r["trend"]]):
                item = QTableWidgetItem(v)
                if r["tag"] == "buy":
                    item.setBackground(QColor("#1A3A2A"))
                elif r["tag"] == "sell":
                    item.setBackground(QColor("#3A1A1A"))
                elif r["tag"] == "hold":
                    item.setBackground(QColor("#3A3A1A"))
                self._table.setItem(row, c, item)
