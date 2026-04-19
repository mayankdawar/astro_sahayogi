"""12-House relative significations (South KP / Cuspal Interlinks) dialog."""
from __future__ import annotations
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from astro_sahayogi.data.constants import SIGN_LORDS
from astro_sahayogi.core.kp.sublords import get_kp_lords


class SouthKPDialog(QDialog):
    def __init__(self, planet_data, cusps, chalit_signs, report_cusps, i18n, parent=None):
        super().__init__(parent)
        self.setWindowTitle("12-House Relative Significations (South KP)")
        self.setMinimumSize(1150, 450)
        self._p_data = planet_data
        self._cusps = cusps
        self._chalit = chalit_signs
        self._report_cusps = report_cusps
        self._i18n = i18n
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        top = QHBoxLayout()
        top.addWidget(QLabel("Select Planet:"))
        self._planet = QComboBox()
        self._planet.addItems(["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"])
        self._planet.currentTextChanged.connect(self._update)
        top.addWidget(self._planet)
        top.addWidget(QLabel("A = Sign Lord | B = Star Lord | C = Sub Lord | D = Sub-Sub Lord"))
        top.addStretch()
        layout.addLayout(top)

        self._table = QTableWidget(12, 5)
        self._table.setHorizontalHeaderLabels(["House", "Self", "Star Lord", "Sub Lord", "S-Sub Lord"])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self._table)
        self._update()

    def _get_abcd(self, pl_name):
        A, B, C, D = [], [], [], []
        if not pl_name or pl_name == "-":
            return A, B, C, D
        trans_pl = self._i18n.tr_p(pl_name)
        for i in range(12):
            h_num = i + 1
            if pl_name not in ("Rahu", "Ketu") and SIGN_LORDS[self._chalit[i] - 1] == pl_name:
                A.append(h_num)
            row = self._report_cusps[i]
            if row[4] == trans_pl:
                B.append(h_num)
            if row[5] == trans_pl:
                C.append(h_num)
            if row[6] == trans_pl:
                D.append(h_num)
        return A, B, C, D

    def _rotate(self, arr, n):
        return sorted([(v - n + 12) % 12 + 1 for v in arr])

    def _fmt(self, A, B, C, D, n):
        rA, rB, rC, rD = self._rotate(A, n), self._rotate(B, n), self._rotate(C, n), self._rotate(D, n)
        parts = []
        if rA:
            parts.append(f"A:{','.join(map(str, rA))}")
        if rB:
            parts.append(f"B:{','.join(map(str, rB))}")
        if rC:
            parts.append(f"C:{','.join(map(str, rC))}")
        if rD:
            parts.append(f"D:{','.join(map(str, rD))}")
        return " | ".join(parts) if parts else "-"

    def _update(self):
        sel = self._planet.currentText()
        p_info = self._p_data.get(sel)
        if not p_info:
            return
        st, sb, ssb = get_kp_lords(p_info["lon"])
        base_self = self._get_abcd(sel)
        base_st = self._get_abcd(st)
        base_sb = self._get_abcd(sb)
        base_ssb = self._get_abcd(ssb)

        self._table.setHorizontalHeaderLabels(
            ["House (As Asc)", f"Self ({sel})", f"Star Lord ({st})", f"Sub Lord ({sb})", f"S-Sub Lord ({ssb})"]
        )

        for i in range(12):
            self._table.setItem(i, 0, QTableWidgetItem(f"House {i+1} as Asc"))
            self._table.setItem(i, 1, QTableWidgetItem(self._fmt(*base_self, i + 1)))
            self._table.setItem(i, 2, QTableWidgetItem(self._fmt(*base_st, i + 1)))
            self._table.setItem(i, 3, QTableWidgetItem(self._fmt(*base_sb, i + 1)))
            self._table.setItem(i, 4, QTableWidgetItem(self._fmt(*base_ssb, i + 1)))
