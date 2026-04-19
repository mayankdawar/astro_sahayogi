"""Degree hits (P2P and P2H) display dialog."""
from __future__ import annotations
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox,
)
from PySide6.QtGui import QColor


class DegreeHitsDialog(QDialog):
    def __init__(self, hit_p2p, hit_p2h, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Degree Hits")
        self.setMinimumSize(950, 650)
        self._build_ui(hit_p2p, hit_p2h)

    def _build_ui(self, p2p, p2h):
        layout = QVBoxLayout(self)

        g1 = QGroupBox("Degree Hits (Planet to Planet)")
        g1_layout = QVBoxLayout(g1)
        self._p2p = QTableWidget(0, 5)
        self._p2p.setHorizontalHeaderLabels(["Planet 1", "Planet 2", "Aspect Type", "Exact Diff", "Nature"])
        self._p2p.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._p2p.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        g1_layout.addWidget(self._p2p)
        layout.addWidget(g1)

        g2 = QGroupBox("Degree Hits (Planet to House)")
        g2_layout = QVBoxLayout(g2)
        self._p2h = QTableWidget(0, 5)
        self._p2h.setHorizontalHeaderLabels(["Planet", "House", "Aspect Type", "Exact Diff", "Nature"])
        self._p2h.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._p2h.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        g2_layout.addWidget(self._p2h)
        layout.addWidget(g2)

        self._fill(self._p2p, p2p)
        self._fill(self._p2h, p2h)

    def _fill(self, table, data):
        for row_data in data:
            row = table.rowCount()
            table.insertRow(row)
            for c, v in enumerate(row_data):
                item = QTableWidgetItem(str(v))
                nature = row_data[4] if len(row_data) > 4 else ""
                if "Positive" in str(nature):
                    item.setForeground(QColor("#27AE60"))
                elif "Negative" in str(nature):
                    item.setForeground(QColor("#E74C3C"))
                table.setItem(row, c, item)

    def update_data(self, p2p, p2h):
        self._p2p.setRowCount(0)
        self._p2h.setRowCount(0)
        self._fill(self._p2p, p2p)
        self._fill(self._p2h, p2h)
