"""Main dashboard screen with charts, tables, dasha, RP, and tabs."""
from __future__ import annotations
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QTabWidget,
    QLabel, QPushButton, QComboBox, QGroupBox, QFrame, QMenu,
    QSizePolicy, QCheckBox,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QAction

from astro_sahayogi.ui.widgets.chart_canvas import ChartCanvas
from astro_sahayogi.ui.widgets.dasha_tree_widget import DashaTreeWidget
from astro_sahayogi.ui.widgets.planet_table import PlanetTable
from astro_sahayogi.ui.widgets.time_control import TimeControl
from astro_sahayogi.ui.widgets.rp_panel import RPPanel
from astro_sahayogi.ui.widgets.nadi_matrix_widget import NadiMatrixWidget
from astro_sahayogi.models.birth_data import BirthData
from astro_sahayogi.utils.time_format import format_local_time


class DashboardScreen(QWidget):
    """Main dashboard: mode bar, charts, data tabs, dasha tree, RP panel, time controls."""

    mode_changed = Signal(str)
    rotation_changed = Signal(int)
    language_changed = Signal(str)
    time_adjusted = Signal(int)
    exit_requested = Signal()
    export_report = Signal()
    save_chart_requested = Signal()
    set_transit_time = Signal()
    set_horary_time = Signal()

    open_forward_check = Signal()
    open_ssub_tracker = Signal()
    open_degree_hits = Signal()
    open_retro_report = Signal()
    open_transit_search = Signal()
    open_btr = Signal()
    open_medical = Signal()
    open_intraday = Signal()
    open_longterm = Signal()
    open_south_kp = Signal()
    open_options = Signal()
    clock_format_changed = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._clock_24h = True
        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self._build_top_bar())

        self.birth_info = QLabel("")
        self.birth_info.setWordWrap(True)
        self.birth_info.setMinimumHeight(36)
        self.birth_info.setStyleSheet(
            "QLabel { background-color: #FFF8EE; color: #444; font-size: 11px; "
            "padding: 8px 14px; border-bottom: 1px solid #D4C5B0; }"
        )
        main_layout.addWidget(self.birth_info)

        content = QSplitter(Qt.Orientation.Horizontal)
        content.setHandleWidth(3)

        left_panel = QSplitter(Qt.Orientation.Vertical)
        left_panel.setHandleWidth(3)

        charts_row = QWidget()
        charts_row.setStyleSheet("QWidget { background: transparent; border: none; }")
        charts_layout = QHBoxLayout(charts_row)
        charts_layout.setContentsMargins(8, 6, 8, 4)
        charts_layout.setSpacing(10)

        self.lagna_canvas = ChartCanvas()
        self.lagna_canvas.setMinimumSize(340, 340)
        self.chalit_canvas = ChartCanvas()
        self.chalit_canvas.setMinimumSize(340, 340)

        lagna_panel = self._make_titled_panel("Lagna Chart", self.lagna_canvas)
        chalit_panel = self._make_titled_panel("Bhava Chalit", self.chalit_canvas)

        charts_layout.addWidget(lagna_panel)
        charts_layout.addWidget(chalit_panel)
        left_panel.addWidget(charts_row)

        self.tabs = QTabWidget()
        p_headers = ["Planet", "Sign", "Degree", "Nakshatra", "Star Lord", "Sub Lord", "S-Sub"]
        c_headers = ["House", "Sign", "Degree", "Nakshatra", "Star Lord", "Sub Lord", "S-Sub"]

        self.planet_table = PlanetTable(p_headers)
        self.cusp_table = PlanetTable(c_headers)
        self.nadi_widget = NadiMatrixWidget()

        tab_positions = QWidget()
        pos_layout = QHBoxLayout(tab_positions)
        pos_layout.setContentsMargins(4, 4, 4, 4)
        pos_layout.setSpacing(8)
        pos_layout.addWidget(self.planet_table)
        pos_layout.addWidget(self.cusp_table)

        self.tabs.addTab(tab_positions, "Positions")
        self.tabs.addTab(self.nadi_widget, "Nadi Signifs")

        left_panel.addWidget(self.tabs)
        left_panel.setSizes([480, 320])
        content.addWidget(left_panel)

        right_panel = QWidget()
        right_panel.setStyleSheet("QWidget { background: transparent; border: none; }")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(4, 6, 8, 6)
        right_layout.setSpacing(8)

        self.dasha_tree = DashaTreeWidget()
        right_layout.addWidget(
            self._make_titled_panel("Vimshottari Dasha (5 Levels)", self.dasha_tree),
            stretch=3,
        )

        self.rp_panel = RPPanel()
        right_layout.addWidget(
            self._make_titled_panel("Live Ruling Planets (RP)", self.rp_panel),
            stretch=1,
        )

        right_panel.setMinimumWidth(380)
        content.addWidget(right_panel)
        content.setSizes([860, 420])

        main_layout.addWidget(content, stretch=1)
        main_layout.addWidget(self._build_time_bar())

    def _build_top_bar(self) -> QFrame:
        top_bar = QFrame()
        top_bar.setObjectName("topBar")
        top_bar.setStyleSheet("""
            QFrame#topBar {
                background-color: #F5F0E8;
                border: none;
                border-radius: 0;
                border-bottom: 2px solid #D4C5B0;
                padding: 0;
            }
        """)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(14, 8, 14, 8)
        top_layout.setSpacing(6)

        self._mode_buttons = {}
        for mode in ["Natal", "Transit", "Horary"]:
            btn = QPushButton(mode)
            btn.setCheckable(True)
            btn.setChecked(mode == "Natal")
            btn.setFixedHeight(32)
            btn.clicked.connect(lambda checked, m=mode: self._on_mode_click(m))
            top_layout.addWidget(btn)
            self._mode_buttons[mode] = btn

        self._add_separator(top_layout)

        lbl = QLabel("Revolve to House:")
        lbl.setStyleSheet("color: #555; font-size: 12px; font-weight: 600;")
        top_layout.addWidget(lbl)
        self.rotate_combo = QComboBox()
        self.rotate_combo.setFixedWidth(65)
        self.rotate_combo.addItems([str(i) for i in range(1, 13)])
        self.rotate_combo.currentTextChanged.connect(lambda v: self.rotation_changed.emit(int(v)))
        top_layout.addWidget(self.rotate_combo)

        self._add_separator(top_layout)

        lbl2 = QLabel("Language:")
        lbl2.setStyleSheet("color: #555; font-size: 12px; font-weight: 600;")
        top_layout.addWidget(lbl2)
        self.lang_combo = QComboBox()
        self.lang_combo.setFixedWidth(100)
        self.lang_combo.addItems(["English", "Hindi"])
        self.lang_combo.currentTextChanged.connect(self.language_changed.emit)
        top_layout.addWidget(self.lang_combo)

        self._add_separator(top_layout)

        self._clock_fmt_chk = QCheckBox("24-hour time")
        self._clock_fmt_chk.setChecked(True)
        self._clock_fmt_chk.setStyleSheet("color: #555; font-size: 12px; font-weight: 600;")
        self._clock_fmt_chk.toggled.connect(self._on_clock_format_toggled)
        top_layout.addWidget(self._clock_fmt_chk)

        top_layout.addStretch()

        adv_btn = QPushButton("Advanced Tools")
        adv_btn.setFixedHeight(32)
        adv_btn.setStyleSheet("""
            QPushButton {
                background-color: #D4760A; color: #FFFFFF;
                font-weight: 700; border: none; border-radius: 6px;
                padding: 6px 16px; font-size: 12px;
            }
            QPushButton:hover { background-color: #B8650A; }
            QPushButton::menu-indicator { image: none; }
        """)
        adv_menu = QMenu(self)
        for label, signal in [
            ("Forward Check", self.open_forward_check),
            ("S-Sub Tracker", self.open_ssub_tracker),
            ("Degree Hits", self.open_degree_hits),
            ("Retro Report", self.open_retro_report),
            ("Advance Transit Search", self.open_transit_search),
            ("Auto-BTR", self.open_btr),
            ("Medical Dashboard", self.open_medical),
            ("Intraday Market", self.open_intraday),
            ("Long-Term Wealth", self.open_longterm),
            ("12-House Links", self.open_south_kp),
        ]:
            action = adv_menu.addAction(label)
            action.triggered.connect(signal.emit)
        adv_btn.setMenu(adv_menu)
        top_layout.addWidget(adv_btn)
        top_layout.addSpacing(4)

        save_dash_btn = QPushButton("\u2193 Save Chart")
        save_dash_btn.setFixedHeight(32)
        save_dash_btn.setToolTip("Save current natal data to the chart database")
        save_dash_btn.clicked.connect(self.save_chart_requested.emit)
        top_layout.addWidget(save_dash_btn)

        report_btn = QPushButton("1-Page Report")
        report_btn.setFixedHeight(32)
        report_btn.clicked.connect(self.export_report.emit)
        top_layout.addWidget(report_btn)

        opts_btn = QPushButton("Options")
        opts_btn.setFixedHeight(32)
        opts_btn.clicked.connect(self.open_options.emit)
        top_layout.addWidget(opts_btn)

        exit_btn = QPushButton("EXIT")
        exit_btn.setFixedHeight(32)
        exit_btn.setProperty("danger", True)
        exit_btn.clicked.connect(self.exit_requested.emit)
        top_layout.addWidget(exit_btn)

        return top_bar

    def _build_time_bar(self) -> QFrame:
        time_bar = QFrame()
        time_bar.setObjectName("timeBar")
        time_bar.setStyleSheet("""
            QFrame#timeBar {
                background-color: #F5F0E8;
                border: none;
                border-radius: 0;
                border-top: 2px solid #D4C5B0;
                padding: 0;
            }
        """)
        time_layout = QHBoxLayout(time_bar)
        time_layout.setContentsMargins(14, 6, 14, 6)
        time_layout.setSpacing(8)

        self.time_control = TimeControl()
        self.time_control.time_adjusted.connect(self.time_adjusted.emit)
        time_layout.addWidget(self.time_control, stretch=1)

        time_layout.addSpacing(8)

        transit_btn = QPushButton("Set Transit")
        transit_btn.setFixedHeight(32)
        transit_btn.setStyleSheet("""
            QPushButton {
                background-color: #2980B9; color: #FFFFFF;
                font-weight: 700; border: none; border-radius: 6px;
                padding: 6px 18px; font-size: 12px;
            }
            QPushButton:hover { background-color: #2471A3; }
        """)
        transit_btn.clicked.connect(self.set_transit_time.emit)
        time_layout.addWidget(transit_btn)

        horary_btn = QPushButton("Set Horary")
        horary_btn.setFixedHeight(32)
        horary_btn.setStyleSheet("""
            QPushButton {
                background-color: #8E44AD; color: #FFFFFF;
                font-weight: 700; border: none; border-radius: 6px;
                padding: 6px 18px; font-size: 12px;
            }
            QPushButton:hover { background-color: #7D3C98; }
        """)
        horary_btn.clicked.connect(self.set_horary_time.emit)
        time_layout.addWidget(horary_btn)

        return time_bar

    def _on_clock_format_toggled(self, checked: bool):
        self._clock_24h = checked
        self.clock_format_changed.emit(checked)

    def set_clock_format_24h(self, use_24: bool):
        self._clock_24h = use_24
        self._clock_fmt_chk.blockSignals(True)
        self._clock_fmt_chk.setChecked(use_24)
        self._clock_fmt_chk.blockSignals(False)

    def clock_format_24h(self) -> bool:
        return self._clock_24h

    def update_birth_summary(self, bd: BirthData, use_24h: bool | None = None):
        if bd is None:
            self.birth_info.setText("")
            return
        u24 = self._clock_24h if use_24h is None else use_24h
        tob_disp = bd.tob
        try:
            parts = bd.tob.replace(" ", ":").split(":")
            h, m = int(parts[0]), int(parts[1])
            s = int(parts[2]) if len(parts) > 2 else 0
            from datetime import datetime

            tt = datetime(2000, 1, 1, h, m, s)
            tob_disp = format_local_time(tt, u24)
        except (ValueError, IndexError):
            pass
        self.birth_info.setText(
            f"{bd.name}  ·  DOB {bd.dob}  ·  Time {tob_disp}  ·  {bd.city}  ·  TZ {bd.timezone}  ·  "
            f"Lat {bd.latitude}  ·  Lon {bd.longitude}  ·  Horary # {bd.horary_number}"
        )

    def _on_mode_click(self, mode: str):
        for m, btn in self._mode_buttons.items():
            btn.setChecked(m == mode)
        self.mode_changed.emit(mode)

    def _add_separator(self, layout: QHBoxLayout):
        sep = QFrame()
        sep.setFixedWidth(1)
        sep.setFixedHeight(22)
        sep.setStyleSheet("background-color: #D4C5B0; border: none; border-radius: 0; padding: 0;")
        layout.addSpacing(8)
        layout.addWidget(sep)
        layout.addSpacing(8)

    def _make_titled_panel(self, title: str, widget: QWidget) -> QFrame:
        """Creates a panel with a visible title label above the widget, avoiding QGroupBox title clipping."""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #D4C5B0;
                border-radius: 8px;
                padding: 0;
            }
        """)
        panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 6, 8, 8)
        layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setFont(QFont("Helvetica Neue", 12, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #8B1A1A; border: none; padding: 0; background: transparent;")
        layout.addWidget(title_label)

        layout.addWidget(widget, stretch=1)
        return panel
