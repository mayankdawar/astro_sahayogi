"""Live ruling planets panel with auto-refresh."""
from __future__ import annotations
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy,
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont


class RPPanel(QWidget):
    """Displays live ruling planets with a 1-second refresh timer."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._paused = False
        self._compute_fn = None
        self._use_24_hour_clock = True

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 4)
        layout.setSpacing(4)

        top = QHBoxLayout()
        self._time_label = QLabel("Loading...")
        self._time_label.setFont(QFont("Helvetica Neue", 12, QFont.Weight.Bold))
        self._time_label.setStyleSheet("color: #8B1A1A; background: transparent; border: none;")
        top.addWidget(self._time_label)
        top.addStretch()

        self._pause_btn = QPushButton("Pause")
        self._pause_btn.setFixedSize(70, 26)
        self._pause_btn.clicked.connect(self._toggle_pause)
        top.addWidget(self._pause_btn)
        layout.addLayout(top)

        self._table = QTableWidget(3, 4)
        self._table.setHorizontalHeaderLabels(["Planet", "Sign L", "Star L", "Sub L"])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._table.horizontalHeader().setMinimumSectionSize(50)
        self._table.horizontalHeader().setMinimumHeight(30)
        self._table.verticalHeader().setVisible(False)
        self._table.verticalHeader().setDefaultSectionSize(24)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setShowGrid(False)
        self._table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self._table.setFixedHeight(120)
        layout.addWidget(self._table)

        self._info_label = QLabel("")
        self._info_label.setFont(QFont("Helvetica Neue", 11, QFont.Weight.Bold))
        self._info_label.setStyleSheet(
            "font-size: 11px; font-weight: bold;"
            "background-color: #FFF3E0;"
            "color: #8B1A1A; padding: 5px 8px; border-radius: 5px;"
            "border: 1px solid #D4C5B0;"
        )
        self._info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._info_label)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh)
        self._timer.start(1000)

    def set_compute_fn(self, fn):
        self._compute_fn = fn

    def set_info_text(self, text: str):
        self._info_label.setText(text)

    def set_use_24_hour_clock(self, use_24: bool):
        self._use_24_hour_clock = use_24

    def set_time_label(self, text: str):
        self._time_label.setText(text)

    def _toggle_pause(self):
        self._paused = not self._paused
        self._pause_btn.setText("Resume" if self._paused else "Pause")

    def _refresh(self):
        if self._paused or not self._compute_fn:
            return
        try:
            data = self._compute_fn()
            now_local = data.get("now_local")
            if now_local is not None:
                from astro_sahayogi.utils.time_format import format_local_time

                tstr = format_local_time(now_local, self._use_24_hour_clock)
            else:
                tstr = data.get("time", "")
            self._time_label.setText(f"Time: {tstr}")
            rows = [
                ("Lagna", data["lagna"]["sign_lord"], data["lagna"]["star_lord"], data["lagna"]["sub_lord"]),
                ("Moon", data["moon"]["sign_lord"], data["moon"]["star_lord"], data["moon"]["sub_lord"]),
                ("Day Lord", data["day_lord"], "-", "-"),
            ]
            for r, row_data in enumerate(rows):
                for c, val in enumerate(row_data):
                    item = QTableWidgetItem(str(val))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    item.setFont(QFont("Helvetica Neue", 10))
                    self._table.setItem(r, c, item)
        except Exception:
            pass

    def stop(self):
        self._timer.stop()
