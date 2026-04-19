"""Birth data input form screen with decorative astrology graphics."""
from __future__ import annotations
import math
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QSpinBox, QFrame, QGraphicsDropShadowEffect,
    QDateEdit, QTimeEdit, QCompleter, QCalendarWidget, QSizePolicy, QButtonGroup,
    QAbstractSpinBox,
)
from PySide6.QtCore import Signal, Qt, QRectF, QPointF, QDate, QTime, QTimer
from PySide6.QtGui import (
    QFont, QColor, QPainter, QPen, QBrush, QLinearGradient,
    QRadialGradient, QPainterPath,
)
import pytz

from astro_sahayogi.models.birth_data import BirthData

ZODIAC_SYMBOLS = [
    "\u2648", "\u2649", "\u264A", "\u264B", "\u264C", "\u264D",
    "\u264E", "\u264F", "\u2650", "\u2651", "\u2652", "\u2653",
]

PLANET_SYMBOLS = ["\u2609", "\u263D", "\u2642", "\u263F", "\u2643", "\u2640", "\u2644"]


class InputScreen(QWidget):
    """Birth data entry form with painted zodiac background art."""

    launch_requested = Signal(BirthData, str)
    save_requested = Signal()
    load_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._time_format_24h = True
        self._build_ui()

    def set_time_format_24h(self, use_24: bool):
        self._time_format_24h = use_24
        self._sync_fmt_buttons()
        self._apply_time_field_format()

    def _sync_fmt_buttons(self):
        if not hasattr(self, "_fmt_group"):
            return
        self._fmt_group.blockSignals(True)
        self._fmt_btn_24.setChecked(self._time_format_24h)
        self._fmt_btn_12.setChecked(not self._time_format_24h)
        self._fmt_group.blockSignals(False)

    def time_format_24h(self) -> bool:
        return self._time_format_24h

    def _apply_time_field_format(self):
        fmt = "HH:mm:ss" if self._time_format_24h else "hh:mm:ss AP"
        self.tob_edit.setDisplayFormat(fmt)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        grad = QLinearGradient(0, 0, 0, h)
        grad.setColorAt(0.0, QColor("#FDF5E6"))
        grad.setColorAt(0.5, QColor("#FFF8EE"))
        grad.setColorAt(1.0, QColor("#F5EDE0"))
        p.fillRect(0, 0, w, h, QBrush(grad))

        self._draw_chart_diamond_watermark(p, w, h)
        self._draw_mini_chart_motifs(p, w, h)
        self._draw_ephemeris_wave(p, w, h)
        self._draw_top_border(p, w)
        self._draw_bottom_border(p, w, h)
        self._draw_zodiac_wheel(p, w, h, left=True)
        self._draw_zodiac_wheel(p, w, h, left=False)
        self._draw_corner_ornaments(p, w, h)
        self._draw_floating_symbols(p, w, h)

        p.end()

    def _draw_top_border(self, p: QPainter, w: int):
        pen = QPen(QColor("#D4760A"), 3)
        p.setPen(pen)
        p.drawLine(40, 20, w - 40, 20)

        pen.setWidth(1)
        pen.setColor(QColor(212, 118, 10, 60))
        p.setPen(pen)
        p.drawLine(60, 26, w - 60, 26)

        cx = w // 2
        diamond_size = 8
        path = QPainterPath()
        path.moveTo(cx, 14)
        path.lineTo(cx + diamond_size, 20)
        path.lineTo(cx, 26)
        path.lineTo(cx - diamond_size, 20)
        path.closeSubpath()
        p.fillPath(path, QBrush(QColor("#D4760A")))

    def _draw_bottom_border(self, p: QPainter, w: int, h: int):
        pen = QPen(QColor("#D4760A"), 3)
        p.setPen(pen)
        p.drawLine(40, h - 20, w - 40, h - 20)

        pen.setWidth(1)
        pen.setColor(QColor(212, 118, 10, 60))
        p.setPen(pen)
        p.drawLine(60, h - 26, w - 60, h - 26)

        p.setFont(QFont("Helvetica Neue", 9))
        p.setPen(QColor(139, 26, 26, 100))
        p.drawText(QRectF(0, h - 50, w, 20), Qt.AlignmentFlag.AlignCenter,
                   "\u2726 Krishnamurti Paddhati \u2726")

    def _draw_zodiac_wheel(self, p: QPainter, w: int, h: int, left: bool):
        cx = 110 if left else w - 110
        cy = h // 2
        outer_r = 90
        inner_r = 55

        rg = QRadialGradient(cx, cy, outer_r)
        rg.setColorAt(0.0, QColor(212, 118, 10, 8))
        rg.setColorAt(0.6, QColor(212, 118, 10, 15))
        rg.setColorAt(1.0, QColor(212, 118, 10, 5))
        p.setBrush(QBrush(rg))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QPointF(cx, cy), outer_r, outer_r)

        p.setPen(QPen(QColor(139, 26, 26, 50), 1.5))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawEllipse(QPointF(cx, cy), outer_r, outer_r)
        p.drawEllipse(QPointF(cx, cy), inner_r, inner_r)

        p.setPen(QPen(QColor(139, 26, 26, 30), 1))
        for i in range(12):
            angle = math.radians(i * 30 - 90)
            x1 = cx + inner_r * math.cos(angle)
            y1 = cy + inner_r * math.sin(angle)
            x2 = cx + outer_r * math.cos(angle)
            y2 = cy + outer_r * math.sin(angle)
            p.drawLine(QPointF(x1, y1), QPointF(x2, y2))

        p.setFont(QFont("Helvetica Neue", 14))
        for i, sym in enumerate(ZODIAC_SYMBOLS):
            angle = math.radians(i * 30 + 15 - 90)
            r = (outer_r + inner_r) / 2
            sx = cx + r * math.cos(angle) - 8
            sy = cy + r * math.sin(angle) - 8
            p.setPen(QColor(139, 26, 26, 45))
            p.drawText(QRectF(sx, sy, 20, 20), Qt.AlignmentFlag.AlignCenter, sym)

        p.setFont(QFont("Helvetica Neue", 10))
        p.setPen(QColor(212, 118, 10, 50))
        planet_r = inner_r * 0.55
        for i, sym in enumerate(PLANET_SYMBOLS):
            angle = math.radians(i * 51.4 - 90)
            sx = cx + planet_r * math.cos(angle) - 7
            sy = cy + planet_r * math.sin(angle) - 7
            p.drawText(QRectF(sx, sy, 18, 18), Qt.AlignmentFlag.AlignCenter, sym)

    def _draw_corner_ornaments(self, p: QPainter, w: int, h: int):
        p.setPen(QPen(QColor(212, 118, 10, 70), 1.5))
        arc_size = 50
        for cx, cy, sa in [
            (25, 25, 0), (w - 25, 25, 90),
            (w - 25, h - 25, 180), (25, h - 25, 270),
        ]:
            p.drawArc(QRectF(cx - arc_size // 2, cy - arc_size // 2, arc_size, arc_size),
                       sa * 16, 90 * 16)

    def _draw_floating_symbols(self, p: QPainter, w: int, h: int):
        p.setFont(QFont("Helvetica Neue", 22))
        p.setPen(QColor(212, 118, 10, 20))

        positions = [
            (w * 0.18, h * 0.15), (w * 0.82, h * 0.12),
            (w * 0.15, h * 0.85), (w * 0.85, h * 0.88),
            (w * 0.08, h * 0.45), (w * 0.92, h * 0.55),
        ]
        symbols = ["\u2609", "\u263D", "\u2642", "\u2643", "\u2640", "\u2644"]
        for (x, y), sym in zip(positions, symbols):
            p.drawText(QRectF(x - 14, y - 14, 30, 30), Qt.AlignmentFlag.AlignCenter, sym)

    def _draw_chart_diamond_watermark(self, p: QPainter, w: int, h: int):
        """Faint North-Indian–style diamond (chart frame) behind the form."""
        cx, cy = w * 0.5, h * 0.52
        s = min(w, h) * 0.36

        def corner(i: int) -> QPointF:
            ang = math.radians(-90 + i * 90)
            return QPointF(cx + s * 0.5 * math.cos(ang), cy + s * 0.5 * math.sin(ang))

        pen = QPen(QColor(139, 90, 40, 20), 1.2)
        p.setPen(pen)
        p.setBrush(Qt.BrushStyle.NoBrush)
        for i in range(4):
            p.drawLine(corner(i), corner((i + 1) % 4))
        p.drawLine(corner(0), corner(2))
        p.drawLine(corner(1), corner(3))
        # Inner chart square (chalit-style hint)
        s2 = s * 0.52

        def corner2(i: int) -> QPointF:
            ang = math.radians(-90 + i * 90)
            return QPointF(cx + s2 * 0.5 * math.cos(ang), cy + s2 * 0.5 * math.sin(ang))

        p.setPen(QPen(QColor(180, 120, 50, 14), 1))
        for i in range(4):
            p.drawLine(corner2(i), corner2((i + 1) % 4))
        # 12 house ticks on outer diamond edge
        p.setPen(QPen(QColor(139, 90, 40, 28), 1))
        for i in range(12):
            ang = math.radians(i * 30 - 90)
            x1 = cx + (s * 0.42) * math.cos(ang)
            y1 = cy + (s * 0.42) * math.sin(ang)
            x2 = cx + (s * 0.50) * math.cos(ang)
            y2 = cy + (s * 0.50) * math.sin(ang)
            p.drawLine(QPointF(x1, y1), QPointF(x2, y2))

    def _draw_mini_chart_motifs(self, p: QPainter, w: int, h: int):
        """Small KP-style diamonds as decorative chart thumbnails."""
        for cx, cy, sz in [
            (w * 0.16, h * 0.26, 52),
            (w * 0.84, h * 0.26, 52),
            (w * 0.12, h * 0.72, 44),
            (w * 0.88, h * 0.72, 44),
        ]:
            self._draw_one_mini_diamond(p, cx, cy, sz)

    def _draw_one_mini_diamond(self, p: QPainter, cx: float, cy: float, size: float):
        s = size

        def cor(i: int) -> QPointF:
            ang = math.radians(-90 + i * 90)
            return QPointF(cx + s * 0.5 * math.cos(ang), cy + s * 0.5 * math.sin(ang))

        p.setPen(QPen(QColor(139, 60, 40, 38), 1.1))
        p.setBrush(QBrush(QColor(255, 248, 235, 28)))
        poly = QPainterPath()
        poly.moveTo(cor(0))
        poly.lineTo(cor(1))
        poly.lineTo(cor(2))
        poly.lineTo(cor(3))
        poly.closeSubpath()
        p.drawPath(poly)
        p.setBrush(Qt.BrushStyle.NoBrush)
        for i in range(4):
            p.drawLine(cor(i), cor((i + 1) % 4))
        p.drawLine(cor(0), cor(2))
        p.drawLine(cor(1), cor(3))

    def _draw_ephemeris_wave(self, p: QPainter, w: int, h: int):
        """Soft planetary-path wave across the lower background."""
        path = QPainterPath()
        y0 = h * 0.86
        path.moveTo(0, y0)
        for x in range(0, w + 1, 8):
            yy = y0 + 10 * math.sin(x * 0.035 + 0.5)
            path.lineTo(x, yy)
        p.setPen(QPen(QColor(212, 118, 10, 45), 1.35))
        p.drawPath(path)
        p.setPen(QPen(QColor(139, 26, 26, 25), 1))
        for x in range(40, w, 90):
            py = y0 + 10 * math.sin(x * 0.035 + 0.5)
            p.drawEllipse(QPointF(x, py), 2.2, 2.2)

    def _make_form_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setMinimumHeight(22)
        lbl.setMaximumHeight(34)
        lbl.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        lbl.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        lbl.setStyleSheet(
            "color: #4a4035; font-size: 12px; font-weight: 600; "
            "padding: 2px 6px 2px 2px; background: transparent; border: none;"
        )
        return lbl

    def _configure_birth_calendar(self):
        cal = self.dob_edit.calendarWidget()
        if cal is None:
            return
        cal.setHorizontalHeaderFormat(
            QCalendarWidget.HorizontalHeaderFormat.ShortDayNames
        )
        cal.setVerticalHeaderFormat(
            QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader
        )
        cal.setNavigationBarVisible(True)
        cal.setGridVisible(True)
        cal.setMinimumSize(320, 270)
        cal.setStyleSheet("""
            QCalendarWidget {
                background-color: #FFFBF5;
                color: #2C2C2C;
                border: 1px solid #C4A574;
                border-radius: 8px;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #8B1A1A;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QCalendarWidget QToolButton {
                color: #FFF8EE;
                background: transparent;
                font-weight: 600;
                border: none;
                padding: 4px 8px;
            }
            QCalendarWidget QToolButton:hover { background-color: rgba(255,255,255,0.12); }
            QCalendarWidget QAbstractItemView:enabled {
                background-color: #FFF8EE;
                color: #2C2C2C;
                selection-background-color: #D4760A;
                selection-color: #FFFFFF;
                outline: none;
            }
            QCalendarWidget QAbstractItemView:disabled { color: #aaa; }
        """)

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setFixedWidth(620)
        card.setObjectName("inputCard")
        card.setStyleSheet("""
            QFrame#inputCard {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 rgba(255, 252, 247, 0.97), stop:0.5 rgba(255, 248, 238, 0.96),
                    stop:1 rgba(255, 241, 224, 0.95));
                border: 2px solid #B8893C;
                border-radius: 18px;
                padding: 22px 24px 24px 24px;
            }
            QFrame#inputGoldRule {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #D4760A, stop:0.5 #F4C430, stop:1 #D4760A);
                border-radius: 3px;
                min-height: 5px;
                max-height: 5px;
            }
            QWidget#timeRowWrap {
                background: transparent;
            }
            QTimeEdit#inputTimeEdit {
                background-color: #FFFFFF;
                color: #2C2C2C;
                border: 1px solid #D4C5B0;
                border-radius: 6px;
                padding: 5px 8px 6px 8px;
                font-size: 10px;
                font-weight: 500;
                min-height: 24px;
            }
            QTimeEdit#inputTimeEdit:focus {
                border: 1px solid #D4760A;
                background-color: #FFFDF8;
            }
            QPushButton#fmtTime24, QPushButton#fmtTime12 {
                border-radius: 6px;
                padding: 4px 6px;
                font-size: 9px;
                font-weight: 700;
                min-height: 24px;
                min-width: 38px;
                max-width: 44px;
            }
            QPushButton#fmtTime24:checked, QPushButton#fmtTime12:checked {
                background-color: #8B1A1A;
                color: #FFF8EE;
                border: 1px solid #6B1010;
            }
            QPushButton#fmtTime24:!checked, QPushButton#fmtTime12:!checked {
                background-color: #FFFFFF;
                color: #555;
                border: 1px solid #D4C5B0;
            }
            QPushButton#fmtTime24:hover:!checked, QPushButton#fmtTime12:hover:!checked {
                border-color: #D4760A;
                background-color: #FFFDF8;
            }
            QDateEdit#inputDateEdit {
                background-color: #FFFDF9;
                border: 1px solid #C4A574;
                border-radius: 8px;
                padding: 5px 8px;
                font-size: 13px;
                font-weight: 600;
                color: #2C2C2C;
                min-height: 34px;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        shadow.setOffset(0, 10)
        shadow.setColor(QColor(100, 80, 50, 80))
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)

        ornament_top = QLabel("\u2726 \u2727 \u2726")
        ornament_top.setFont(QFont("Helvetica Neue", 14))
        ornament_top.setStyleSheet("color: #D4760A; background: transparent; border: none;")
        ornament_top.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(ornament_top)

        title = QLabel("Astro Sahayogi")
        title.setFont(QFont("Helvetica Neue", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: #8B1A1A; background: transparent; border: none;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)

        subtitle = QLabel("KP Astrology Professional Suite")
        subtitle.setFont(QFont("Helvetica Neue", 11))
        subtitle.setStyleSheet("color: #999; background: transparent; border: none; letter-spacing: 2px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(subtitle)

        gold_rule = QFrame()
        gold_rule.setObjectName("inputGoldRule")
        card_layout.addWidget(gold_rule)

        divider = QFrame()
        divider.setFixedHeight(2)
        divider.setStyleSheet("background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 transparent, stop:0.3 #D4760A, stop:0.7 #D4760A, stop:1 transparent); border: none; border-radius: 0; padding: 0;")
        card_layout.addWidget(divider)
        card_layout.addSpacing(4)

        form = QFormLayout()
        form.setSpacing(4)
        form.setVerticalSpacing(8)
        form.setHorizontalSpacing(12)
        form.setContentsMargins(4, 8, 4, 4)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint)

        self.name_edit = QLineEdit("Happy")

        self.dob_edit = QDateEdit()
        self.dob_edit.setObjectName("inputDateEdit")
        self.dob_edit.setCalendarPopup(True)
        self.dob_edit.setDisplayFormat("dd-MM-yyyy")
        self.dob_edit.setDate(QDate.currentDate())
        self._configure_birth_calendar()

        self.tob_edit = QTimeEdit()
        self.tob_edit.setObjectName("inputTimeEdit")
        self.tob_edit.setDisplayFormat("HH:mm:ss")
        self.tob_edit.setTime(QTime.currentTime())
        self.tob_edit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.tob_edit.setFont(QFont("Helvetica Neue", 10, QFont.Weight.Normal))
        self.tob_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self._fmt_btn_24 = QPushButton("24h")
        self._fmt_btn_24.setObjectName("fmtTime24")
        self._fmt_btn_24.setCheckable(True)
        self._fmt_btn_24.setToolTip("24-hour clock")

        self._fmt_btn_12 = QPushButton("12h")
        self._fmt_btn_12.setObjectName("fmtTime12")
        self._fmt_btn_12.setCheckable(True)
        self._fmt_btn_12.setToolTip("12-hour clock with AM/PM")

        self._fmt_group = QButtonGroup(self)
        self._fmt_group.setExclusive(True)
        self._fmt_group.addButton(self._fmt_btn_24, 0)
        self._fmt_group.addButton(self._fmt_btn_12, 1)
        self._fmt_group.idClicked.connect(self._on_time_format_group)

        time_row = QWidget()
        time_row.setObjectName("timeRowWrap")
        time_row.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        time_row.setFixedHeight(32)
        ts = QHBoxLayout(time_row)
        ts.setContentsMargins(0, 0, 0, 0)
        ts.setSpacing(6)
        ts.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        ts.addWidget(self.tob_edit, stretch=1)
        ts.addWidget(self._fmt_btn_24)
        ts.addWidget(self._fmt_btn_12)
        self._sync_fmt_buttons()

        self.city_edit = QLineEdit("Ludhiana")
        self.city_edit.editingFinished.connect(self._maybe_apply_city_from_field)
        QTimer.singleShot(0, self._setup_city_completer)

        self.lat_edit = QLineEdit("30.9010")
        self.lon_edit = QLineEdit("75.8573")
        self.horary_edit = QSpinBox()
        self.horary_edit.setRange(1, 2193)
        self.horary_edit.setValue(1)

        field_icons = [
            ("\u263D", "Name", self.name_edit),
            ("\u2609", "Date of birth", self.dob_edit),
            ("\u231A", "Time of birth", time_row),
            ("\u2302", "City (type to search)", self.city_edit),
            ("\u2195", "Latitude", self.lat_edit),
            ("\u2194", "Longitude", self.lon_edit),
            ("\u2316", "Horary number", self.horary_edit),
        ]
        for icon, label_text, widget in field_icons:
            form.addRow(self._make_form_label(f"{icon}  {label_text}"), widget)

        self.tz_combo = QComboBox()
        self.tz_combo.addItems(pytz.common_timezones)
        self.tz_combo.setCurrentText("Asia/Kolkata")
        form.addRow(self._make_form_label("\u2316  Timezone"), self.tz_combo)

        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English", "Hindi"])
        form.addRow(self._make_form_label("\U0001F310  Language"), self.lang_combo)

        card_layout.addLayout(form)

        divider2 = QFrame()
        divider2.setFixedHeight(1)
        divider2.setStyleSheet("background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 transparent, stop:0.2 #D4C5B0, stop:0.8 #D4C5B0, stop:1 transparent); border: none; border-radius: 0; padding: 0;")
        card_layout.addWidget(divider2)
        card_layout.addSpacing(4)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        fetch_btn = QPushButton("\u2316 Get Location")
        fetch_btn.setFixedHeight(36)
        fetch_btn.clicked.connect(self._on_fetch)
        btn_row.addWidget(fetch_btn)

        save_btn = QPushButton("\u2193 Save Chart")
        save_btn.setFixedHeight(36)
        save_btn.clicked.connect(self.save_requested.emit)
        btn_row.addWidget(save_btn)

        load_btn = QPushButton("\u2191 Open Chart")
        load_btn.setFixedHeight(36)
        load_btn.clicked.connect(self.load_requested.emit)
        btn_row.addWidget(load_btn)

        launch_btn = QPushButton("\u2726  OPEN DASHBOARD")
        launch_btn.setFixedHeight(42)
        launch_btn.setProperty("accent", True)
        launch_btn.clicked.connect(self._on_launch)
        btn_row.addWidget(launch_btn)

        card_layout.addLayout(btn_row)

        ornament_bottom = QLabel("\u2605 \u2606 \u2605")
        ornament_bottom.setFont(QFont("Helvetica Neue", 10))
        ornament_bottom.setStyleSheet("color: #D4760A; background: transparent; border: none;")
        ornament_bottom.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(ornament_bottom)

        self._apply_time_field_format()
        outer.addWidget(card)

    def _on_time_format_group(self, button_id: int):
        self._time_format_24h = button_id == 0
        self._apply_time_field_format()

    def _set_time_format(self, use_24: bool):
        self._time_format_24h = use_24
        self._sync_fmt_buttons()
        self._apply_time_field_format()

    def _setup_city_completer(self):
        from astro_sahayogi.core.location.suggestions import all_city_labels_for_completer

        cities = all_city_labels_for_completer()
        completer = QCompleter(cities, self.city_edit)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setMaxVisibleItems(11)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        completer.activated[str].connect(self._on_city_suggestion_chosen)
        popup = completer.popup()
        popup.setMinimumWidth(420)
        popup.setFont(QFont("Helvetica Neue", 12))
        popup.setStyleSheet(
            "QAbstractItemView { background: #FFFBF5; color: #2C2C2C; "
            "selection-background-color: #D4760A; selection-color: #FFFFFF; "
            "border: 1px solid #C4A574; border-radius: 6px; padding: 2px; font-size: 12px; "
            "outline: none; }"
            "QAbstractItemView::item { min-height: 30px; padding: 6px 10px; }"
        )
        self.city_edit.setCompleter(completer)

    def _on_city_suggestion_chosen(self, text: str):
        self._apply_city_coords(text)

    def _maybe_apply_city_from_field(self):
        self._apply_city_coords(self.city_edit.text().strip())

    def _apply_city_coords(self, text: str):
        from astro_sahayogi.core.location.suggestions import coords_for_suggestion_label

        data = coords_for_suggestion_label(text)
        if not data:
            return
        self.lat_edit.setText(f"{data['lat']:.4f}")
        self.lon_edit.setText(f"{data['lon']:.4f}")
        tz = data.get("timezone")
        if tz and self.tz_combo.findText(tz) >= 0:
            self.tz_combo.setCurrentText(tz)

    def get_birth_data(self) -> BirthData:
        dob_str = self.dob_edit.date().toString("dd-MM-yyyy")
        tob_str = self.tob_edit.time().toString("HH:mm:ss")
        return BirthData(
            name=self.name_edit.text().strip(),
            dob=dob_str,
            tob=tob_str,
            city=self.city_edit.text().strip(),
            latitude=float(self.lat_edit.text() or 0),
            longitude=float(self.lon_edit.text() or 0),
            timezone=self.tz_combo.currentText(),
            horary_number=self.horary_edit.value(),
        )

    def set_birth_data(self, bd: BirthData):
        self.name_edit.setText(bd.name)
        d = QDate.fromString(bd.dob, "dd-MM-yyyy")
        if d.isValid():
            self.dob_edit.setDate(d)
        t = QTime.fromString(bd.tob, "HH:mm:ss")
        if not t.isValid():
            t = QTime.fromString(bd.tob, "h:mm:ss AP")
        if t.isValid():
            self.tob_edit.setTime(t)
        self.city_edit.setText(bd.city)
        self.lat_edit.setText(str(bd.latitude))
        self.lon_edit.setText(str(bd.longitude))
        self.tz_combo.setCurrentText(bd.timezone)
        self.horary_edit.setValue(bd.horary_number)

    def _on_fetch(self):
        from astro_sahayogi.core.location.resolver import LocationResolver
        resolver = LocationResolver()
        raw = self.city_edit.text().strip()
        city_part = raw.split(",")[0].strip() or raw
        result = resolver.resolve(city_part)
        if result:
            self.lat_edit.setText(f"{result['lat']:.4f}")
            self.lon_edit.setText(f"{result['lon']:.4f}")
            self.tz_combo.setCurrentText(result["timezone"])

    def _on_launch(self):
        bd = self.get_birth_data()
        self.launch_requested.emit(bd, self.lang_combo.currentText())
