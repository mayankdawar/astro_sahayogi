"""Time setter dialog for Transit/Horary mode."""
from __future__ import annotations
from datetime import datetime
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
)
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont

from astro_sahayogi.utils.date_utils import parse_smart_dt


class TimeDialog(QDialog):
    time_set = Signal(datetime)

    def __init__(self, mode_target: str, current_time: datetime | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Set {mode_target} Date/Time")
        self.setFixedSize(300, 220)
        self._build_ui(mode_target, current_time)

    def _build_ui(self, mode_target, current_time):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Date (DD MM YYYY):"))
        self._date = QLineEdit()
        if current_time:
            self._date.setText(current_time.strftime("%d-%m-%Y"))
        layout.addWidget(self._date)

        layout.addWidget(QLabel("Time (HH MM SS):"))
        self._time = QLineEdit()
        if current_time:
            self._time.setText(current_time.strftime("%H:%M:%S"))
        layout.addWidget(self._time)

        btn = QPushButton("Apply Time")
        btn.setProperty("accent", True)
        btn.clicked.connect(self._apply)
        layout.addWidget(btn)

    def _apply(self):
        try:
            dt = parse_smart_dt(f"{self._date.text()} {self._time.text()}")
            self.time_set.emit(dt)
            self.accept()
        except ValueError:
            pass
