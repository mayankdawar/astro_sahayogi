"""Options dialog for ayanamsa and Rahu node selection."""
from __future__ import annotations
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton,
    QButtonGroup, QGroupBox,
)
from PySide6.QtCore import Signal

from astro_sahayogi.data.constants import AYANAMSA_OPTIONS


class OptionsDialog(QDialog):
    settings_changed = Signal(str, str)  # ayanamsa, rahu_mode

    def __init__(self, current_ayanamsa: str, current_rahu: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Options")
        self.setMinimumSize(500, 300)
        self._build_ui(current_ayanamsa, current_rahu)

    def _build_ui(self, aya, rahu):
        layout = QVBoxLayout(self)
        main = QHBoxLayout()

        aya_group = QGroupBox("Ayanamsa Selection")
        aya_layout = QVBoxLayout(aya_group)
        self._aya_group = QButtonGroup(self)
        for opt in AYANAMSA_OPTIONS:
            rb = QRadioButton(opt)
            if opt == aya:
                rb.setChecked(True)
            self._aya_group.addButton(rb)
            aya_layout.addWidget(rb)
        main.addWidget(aya_group)

        node_group = QGroupBox("Rahu's Position")
        node_layout = QVBoxLayout(node_group)
        self._rahu_group = QButtonGroup(self)
        for opt in ["Mean", "TrueNode"]:
            rb = QRadioButton(opt)
            if opt == rahu:
                rb.setChecked(True)
            self._rahu_group.addButton(rb)
            node_layout.addWidget(rb)
        main.addWidget(node_group)
        layout.addLayout(main)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.reject)
        btn_row.addWidget(cancel)
        ok = QPushButton("OK")
        ok.setProperty("accent", True)
        ok.clicked.connect(self._on_ok)
        btn_row.addWidget(ok)
        layout.addLayout(btn_row)

    def _on_ok(self):
        aya = self._aya_group.checkedButton().text()
        rahu = self._rahu_group.checkedButton().text()
        self.settings_changed.emit(aya, rahu)
        self.accept()
