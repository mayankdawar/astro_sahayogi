"""Time adjustment control bar (Year/Month/Week/.../1Sec +/-)."""
from __future__ import annotations
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal, Qt


INTERVALS = [
    ("Year", 31536000), ("Month", 2592000), ("Week", 604800),
    ("Day", 86400), ("Hour", 3600), ("10 Min", 600),
    ("1 Min", 60), ("1 Sec", 1),
]


class TimeControl(QWidget):
    """Emits time_adjusted(seconds_delta) when +/- buttons are clicked."""

    time_adjusted = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        for label, seconds in INTERVALS:
            btn_minus = QPushButton("\u2212")
            btn_minus.setFixedSize(26, 26)
            btn_minus.setStyleSheet("""
                QPushButton {
                    background-color: #C0392B; color: #FFFFFF;
                    font-size: 14px; font-weight: bold; border-radius: 5px;
                    border: none; padding: 0; min-height: 0;
                }
                QPushButton:hover { background-color: #A93226; }
            """)
            btn_minus.clicked.connect(lambda checked, s=-seconds: self.time_adjusted.emit(s))

            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFixedWidth(42)
            lbl.setStyleSheet("font-size: 10px; font-weight: 600; color: #555; background: transparent; border: none;")

            btn_plus = QPushButton("+")
            btn_plus.setFixedSize(26, 26)
            btn_plus.setStyleSheet("""
                QPushButton {
                    background-color: #D4760A; color: #FFFFFF;
                    font-size: 14px; font-weight: bold; border-radius: 5px;
                    border: none; padding: 0; min-height: 0;
                }
                QPushButton:hover { background-color: #B8650A; }
            """)
            btn_plus.clicked.connect(lambda checked, s=seconds: self.time_adjusted.emit(s))

            layout.addWidget(btn_minus)
            layout.addWidget(lbl)
            layout.addWidget(btn_plus)
            layout.addSpacing(2)
