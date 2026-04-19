"""Client database browser screen."""
from __future__ import annotations
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog,
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont

from astro_sahayogi.ui.widgets.search_bar import SearchBar
from astro_sahayogi.models.client import Client


class ClientListScreen(QDialog):
    """Modal dialog for browsing and selecting saved charts."""

    client_selected = Signal(Client)

    def __init__(self, clients: list[Client], parent=None):
        super().__init__(parent)
        self.setWindowTitle("Open Saved Chart")
        self.setMinimumSize(750, 450)
        self._clients = clients

        layout = QVBoxLayout(self)
        title = QLabel("Select a Chart to Open")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self._search = SearchBar("Search Name / City / DOB...")
        self._search.search_changed.connect(self._filter)
        layout.addWidget(self._search)

        headers = ["ID", "Name", "DOB", "Time", "City", "Saved On"]
        self._table = QTableWidget(0, len(headers))
        self._table.setHorizontalHeaderLabels(headers)
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.doubleClicked.connect(self._on_select)
        layout.addWidget(self._table)

        btn = QPushButton("Open Selected Chart")
        btn.setProperty("accent", True)
        btn.clicked.connect(self._on_select)
        layout.addWidget(btn)

        self._populate(self._clients)

    def _populate(self, clients: list[Client]):
        self._table.setRowCount(0)
        for c in clients:
            row = self._table.rowCount()
            self._table.insertRow(row)
            for col, val in enumerate([str(c.id or ""), c.name, c.dob, c.tob, c.city, c.created_at or ""]):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self._table.setItem(row, col, item)

    def _filter(self, term: str):
        term = term.lower()
        filtered = [c for c in self._clients
                     if term in (c.name or "").lower()
                     or term in (c.city or "").lower()
                     or term in (c.dob or "")]
        self._populate(filtered)

    def _on_select(self):
        row = self._table.currentRow()
        if row < 0:
            return
        client_id_text = self._table.item(row, 0).text()
        for c in self._clients:
            if str(c.id) == client_id_text:
                self.client_selected.emit(c)
                self.accept()
                return
