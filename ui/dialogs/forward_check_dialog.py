"""Forward checking of planet dialog."""
from __future__ import annotations
from datetime import datetime
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QRadioButton, QButtonGroup, QGroupBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from astro_sahayogi.core.analysis.forward_check import run_forward_check
from astro_sahayogi.data.constants import ZODIAC, NAKSHATRAS


class ForwardCheckDialog(QDialog):
    def __init__(self, timezone_str, ayanamsa, planet_map, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Forward Checking of Planet")
        self.setMinimumSize(700, 400)
        self._tz = timezone_str
        self._aya = ayanamsa
        self._pmap = planet_map
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        top = QHBoxLayout()
        top.addWidget(QLabel("Planet:"))
        self._planet = QComboBox()
        self._planet.addItems(["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"])
        top.addWidget(self._planet)
        top.addWidget(QLabel("Start Date:"))
        self._date = QLineEdit(datetime.now().strftime("%d-%m-%Y"))
        top.addWidget(self._date)
        layout.addLayout(top)

        target_group = QGroupBox("Target Type")
        tg_layout = QHBoxLayout(target_group)
        self._type_group = QButtonGroup(self)
        for txt in ["Sign", "Nakshatra", "Degree"]:
            rb = QRadioButton(txt)
            self._type_group.addButton(rb)
            tg_layout.addWidget(rb)
            if txt == "Sign":
                rb.setChecked(True)
        layout.addWidget(target_group)

        val_row = QHBoxLayout()
        val_row.addWidget(QLabel("Target Index / Degree:"))
        self._target_val = QLineEdit("0")
        val_row.addWidget(self._target_val)
        layout.addLayout(val_row)

        self._result = QLabel("")
        self._result.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self._result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._result)

        btn = QPushButton("Start Checking")
        btn.setProperty("accent", True)
        btn.clicked.connect(self._run)
        layout.addWidget(btn)

    def _run(self):
        self._result.setText("Calculating...")
        target_type = self._type_group.checkedButton().text()
        try:
            target_val = float(self._target_val.text())
        except ValueError:
            target_val = 0

        result = run_forward_check(
            self._planet.currentText(), self._pmap, target_type, target_val,
            self._date.text(), self._tz, self._aya,
        )
        if result:
            self._result.setText(f"{self._planet.currentText()} enters target around {result}")
            self._result.setStyleSheet("color: #27AE60;")
        else:
            self._result.setText("Target not reached within 100 years.")
            self._result.setStyleSheet("color: #E74C3C;")
