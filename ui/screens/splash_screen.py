"""Splash screen with branding and license check."""
from __future__ import annotations
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont


class SplashScreen(QWidget):
    """Branded splash shown on startup while license is verified."""

    ready = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(520, 340)
        self.setStyleSheet("background-color: #8B1A1A; border-radius: 14px;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(8)

        title = QLabel("Astro Sahayogi")
        title.setFont(QFont("Helvetica Neue", 32, QFont.Weight.Bold))
        title.setStyleSheet("color: #FDF5E6; background: transparent;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("KP Astrology Professional Suite")
        subtitle.setFont(QFont("Helvetica Neue", 13))
        subtitle.setStyleSheet("color: #E8C9A0; background: transparent;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(36)

        self._progress = QProgressBar()
        self._progress.setRange(0, 100)
        self._progress.setValue(0)
        self._progress.setFixedWidth(320)
        self._progress.setFixedHeight(8)
        self._progress.setTextVisible(False)
        self._progress.setStyleSheet("""
            QProgressBar {
                background-color: rgba(255, 255, 255, 0.15);
                border: none;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #D4760A, stop:1 #E8A54B);
                border-radius: 4px;
            }
        """)
        layout.addWidget(self._progress, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(8)

        self._status = QLabel("Initializing...")
        self._status.setStyleSheet("color: #E8C9A0; font-size: 11px; background: transparent;")
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._status)

        self._step = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._advance)
        self._timer.start(30)

    def _advance(self):
        self._step += 2
        self._progress.setValue(min(self._step, 100))
        if self._step < 30:
            self._status.setText("Loading ephemeris data...")
        elif self._step < 60:
            self._status.setText("Initializing computation engine...")
        elif self._step < 90:
            self._status.setText("Preparing UI components...")
        else:
            self._status.setText("Ready!")

        if self._step >= 100:
            self._timer.stop()
            self.ready.emit()
