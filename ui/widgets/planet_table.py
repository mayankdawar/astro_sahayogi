"""Reusable planet/cusp positions table."""
from __future__ import annotations
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt

from astro_sahayogi.data.colors import get_planet_color


class PlanetTable(QTableWidget):
    """Generic table for planet or cusp position rows with draggable column headers."""

    def __init__(self, headers: list[str], parent=None):
        super().__init__(parent)
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        h = self.horizontalHeader()
        h.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        h.setStretchLastSection(True)
        h.setMinimumSectionSize(50)
        h.setDefaultSectionSize(90)
        h.setMinimumHeight(32)
        h.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(28)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        self.setWordWrap(False)

    def load_rows(self, rows: list[tuple]):
        self.setRowCount(0)
        for row_data in rows:
            row_idx = self.rowCount()
            self.insertRow(row_idx)
            for col, val in enumerate(row_data):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                font = QFont("Helvetica Neue", 11)
                if col == 0:
                    color = get_planet_color(str(val))
                    item.setForeground(QColor(color))
                    font.setWeight(QFont.Weight.Bold)
                else:
                    item.setForeground(QColor("#2C2C2C"))
                item.setFont(font)
                self.setItem(row_idx, col, item)
        self.resizeColumnsToContents()
