"""Retrograde/Direct report dialog."""
from __future__ import annotations
from datetime import datetime, timedelta
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
)
from PySide6.QtGui import QFont

from astro_sahayogi.core.analysis.retro_report import generate_retro_report


class RetroReportDialog(QDialog):
    def __init__(self, ayanamsa, planet_map, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Planet Retro/Direct Report")
        self.setMinimumSize(600, 500)
        self._aya = ayanamsa
        self._pmap = planet_map
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        top = QHBoxLayout()
        self._from = QLineEdit(datetime.now().strftime("%d-%m-%Y"))
        self._to = QLineEdit((datetime.now() + timedelta(days=365)).strftime("%d-%m-%Y"))
        self._planet = QComboBox()
        self._planet.addItems(["Mercury", "Venus", "Mars", "Jupiter", "Saturn"])
        for label, w in [("From:", self._from), ("To:", self._to)]:
            top.addWidget(QLabel(label))
            top.addWidget(w)
        top.addWidget(self._planet)
        btn = QPushButton("Generate")
        btn.setProperty("accent", True)
        btn.clicked.connect(self._run)
        top.addWidget(btn)
        layout.addLayout(top)

        self._table = QTableWidget(0, 2)
        self._table.setHorizontalHeaderLabels(["Date", "Movement Change"])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self._table)

    def _run(self):
        self._table.setRowCount(0)
        results = generate_retro_report(self._planet.currentText(), self._pmap, self._from.text(), self._to.text(), self._aya)
        for r in results:
            row = self._table.rowCount()
            self._table.insertRow(row)
            self._table.setItem(row, 0, QTableWidgetItem(r["date"]))
            self._table.setItem(row, 1, QTableWidgetItem(r["status"]))
