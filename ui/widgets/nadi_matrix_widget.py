"""Scrollable Nadi significator grid widget."""
from __future__ import annotations
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt


class NadiMatrixWidget(QTableWidget):
    """Displays the Nadi significator matrix with draggable column headers."""

    HEADERS = ["Planet", "P-Signifs", "Star Lord", "St-Signifs", "Sub Lord", "Sb-Signifs", "Star L Of", "Sub L Of"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(len(self.HEADERS))
        self.setHorizontalHeaderLabels(self.HEADERS)
        h = self.horizontalHeader()
        h.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        h.setStretchLastSection(True)
        h.setMinimumSectionSize(55)
        h.setDefaultSectionSize(85)
        h.setMinimumHeight(32)
        h.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(28)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        self.setWordWrap(False)

    def load_data(self, nadi_rows: list[tuple], cusp_rows: list[tuple]):
        from astro_sahayogi.data.constants import NADI_ORDER

        star_lord_of: dict[str, list[str]] = {}
        sub_lord_of: dict[str, list[str]] = {}

        for row in cusp_rows:
            h_num = str(row[0])
            if row[4] not in star_lord_of:
                star_lord_of[row[4]] = []
            star_lord_of[row[4]].append(h_num)
            if row[5] not in sub_lord_of:
                sub_lord_of[row[5]] = []
            sub_lord_of[row[5]].append(h_num)

        self.setRowCount(len(nadi_rows))
        for r, row in enumerate(nadi_rows):
            p_name = row[0]
            st_houses = ", ".join(star_lord_of.get(p_name, [])) or "-"
            sb_houses = ", ".join(sub_lord_of.get(p_name, [])) or "-"

            full_row = list(row) + [st_houses, sb_houses]
            for c, val in enumerate(full_row):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if c == 0:
                    item.setFont(QFont("Helvetica Neue", 11, QFont.Weight.Bold))
                else:
                    item.setFont(QFont("Helvetica Neue", 11))
                    item.setForeground(QColor("#2C2C2C"))
                self.setItem(r, c, item)
        self.resizeColumnsToContents()
