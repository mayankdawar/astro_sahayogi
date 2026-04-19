"""Vimshottari dasha tree with lazy loading."""
from __future__ import annotations
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView
from PySide6.QtGui import QColor, QBrush, QFont
from PySide6.QtCore import Signal, Qt

from astro_sahayogi.models.dasha_node import DashaNode
from astro_sahayogi.data.colors import DASHA_LORD_COLORS


class DashaTreeWidget(QTreeWidget):
    """Lazy-loading dasha tree that emits dasha_selected with the chain.

    Uses the same visual treatment as PlanetTable: no grid lines,
    alternating row colours, interactive/stretch header sizing, and
    a 32 px minimum header height to avoid vertical clipping.
    """

    dasha_selected = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderLabels(["Dasha Lord", "Start Date", "End Date"])

        header = self.header()
        header.setMinimumHeight(32)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        header.setMinimumSectionSize(90)
        header.resizeSection(1, 120)
        header.resizeSection(2, 120)

        self.setIndentation(14)
        self.setAnimated(True)
        self.setRootIsDecorated(True)
        self.setAlternatingRowColors(True)
        self.setWordWrap(False)

        self.itemExpanded.connect(self._on_expand)
        self.itemClicked.connect(self._on_select)
        self._node_map: dict[int, DashaNode] = {}
        self._generate_children_fn = None

    def set_generator(self, fn):
        """Set the function to generate child dasha periods."""
        self._generate_children_fn = fn

    def load_mahadashas(self, nodes: list[DashaNode]):
        self.clear()
        self._node_map.clear()
        active_item = None
        for node in nodes:
            item = self._create_item(node)
            self.addTopLevelItem(item)
            placeholder = QTreeWidgetItem([""])
            item.addChild(placeholder)
            if node.is_active:
                active_item = item

        if active_item:
            self.scrollToItem(active_item)
            active_item.setExpanded(True)

    def _create_item(self, node: DashaNode) -> QTreeWidgetItem:
        item = QTreeWidgetItem([
            node.lord_name,
            node.start.strftime("%d-%m-%Y"),
            node.end.strftime("%d-%m-%Y"),
        ])
        node_id = id(item)
        self._node_map[node_id] = node

        color = DASHA_LORD_COLORS.get(node.lord_name, "#2C2C2C")
        item.setForeground(0, QBrush(QColor(color)))
        item.setFont(0, QFont("Helvetica Neue", 11, QFont.Weight.DemiBold))
        item.setForeground(1, QBrush(QColor("#2C2C2C")))
        item.setFont(1, QFont("Helvetica Neue", 10))
        item.setForeground(2, QBrush(QColor("#2C2C2C")))
        item.setFont(2, QFont("Helvetica Neue", 10))
        item.setTextAlignment(1, Qt.AlignmentFlag.AlignCenter)
        item.setTextAlignment(2, Qt.AlignmentFlag.AlignCenter)

        if node.is_active:
            active_bg = QBrush(QColor("#FFF3E0"))
            for col in range(3):
                item.setBackground(col, active_bg)
            item.setFont(0, QFont("Helvetica Neue", 11, QFont.Weight.Bold))

        return item

    def _on_expand(self, item: QTreeWidgetItem):
        if item.childCount() == 1 and item.child(0).text(0) == "":
            item.removeChild(item.child(0))
            node = self._node_map.get(id(item))
            if node and self._generate_children_fn and node.level < 5:
                children = self._generate_children_fn(
                    node.chain, node.start, node.level, None,
                )
                for child_node in children:
                    child_item = self._create_item(child_node)
                    item.addChild(child_item)
                    if child_node.level < 5:
                        child_item.addChild(QTreeWidgetItem([""]))
                    if child_node.is_active:
                        self.scrollToItem(child_item)
                        child_item.setExpanded(True)

    def _on_select(self, item: QTreeWidgetItem, column: int):
        chain = []
        current = item
        while current:
            node = self._node_map.get(id(current))
            if node:
                chain.insert(0, node)
            current = current.parent()
        self.dasha_selected.emit(chain)
