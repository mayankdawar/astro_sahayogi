"""Filterable search input widget."""
from __future__ import annotations
from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Signal


class SearchBar(QLineEdit):
    """Emits search_changed(str) on every keystroke for live filtering."""

    search_changed = Signal(str)

    def __init__(self, placeholder: str = "Search...", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.textChanged.connect(self.search_changed.emit)
        self.setClearButtonEnabled(True)
