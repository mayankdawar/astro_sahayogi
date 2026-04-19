"""App orchestrator: screen navigation and top-level wiring."""
from __future__ import annotations
import os
import sys
from datetime import datetime
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox
from PySide6.QtCore import Qt

from astro_sahayogi.core.facade import AstrologyEngine
from astro_sahayogi.services.settings import SettingsManager
from astro_sahayogi.services.client_repo import ClientRepository
from astro_sahayogi.ui.screens.input_screen import InputScreen
from astro_sahayogi.ui.screens.dashboard_screen import DashboardScreen
from astro_sahayogi.ui.screens.client_list_screen import ClientListScreen
from astro_sahayogi.ui.controllers.input_controller import InputController
from astro_sahayogi.ui.controllers.dashboard_controller import DashboardController
from astro_sahayogi.ui.controllers.rp_controller import RPController
from astro_sahayogi.ui.controllers.export_controller import ExportController
from astro_sahayogi.ui.dialogs.options_dialog import OptionsDialog
from astro_sahayogi.ui.dialogs.time_dialog import TimeDialog
from astro_sahayogi.ui.dialogs.medical_dialog import MedicalDialog
from astro_sahayogi.ui.dialogs.market_intraday_dialog import IntradayDialog
from astro_sahayogi.ui.dialogs.market_longterm_dialog import LongtermDialog
from astro_sahayogi.ui.dialogs.btr_dialog import BTRDialog
from astro_sahayogi.ui.dialogs.forward_check_dialog import ForwardCheckDialog
from astro_sahayogi.ui.dialogs.retro_report_dialog import RetroReportDialog
from astro_sahayogi.ui.dialogs.degree_hits_dialog import DegreeHitsDialog
from astro_sahayogi.ui.dialogs.ssub_tracker_dialog import SSubTrackerDialog
from astro_sahayogi.ui.dialogs.transit_search_dialog import TransitSearchDialog
from astro_sahayogi.ui.dialogs.south_kp_dialog import SouthKPDialog
from astro_sahayogi.models.birth_data import BirthData
from astro_sahayogi.utils.date_utils import parse_smart_dt


class AstroSahayogiApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Astro Sahayogi - KP Astrology Professional Suite")
        self.setMinimumSize(1450, 950)

        self._engine = AstrologyEngine()
        self._settings = SettingsManager()
        self._client_repo = ClientRepository()
        self._input_ctrl = InputController(self._settings, self._client_repo)
        self._dash_ctrl = DashboardController(self._engine)
        self._export_ctrl = ExportController(self)

        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)

        self._input_screen = InputScreen()
        self._dashboard_screen = DashboardScreen()

        self._stack.addWidget(self._input_screen)
        self._stack.addWidget(self._dashboard_screen)

        self._connect_input()
        self._connect_dashboard()
        self._load_initial_settings()

    def _load_initial_settings(self):
        self._settings.load()
        bd = self._input_ctrl.load_settings()
        self._input_screen.set_birth_data(bd)
        self._input_screen.set_time_format_24h(
            bool(self._settings.get("time_format_24h", True)),
        )

    def _connect_input(self):
        self._input_screen.launch_requested.connect(self._on_launch)
        self._input_screen.save_requested.connect(self._on_save_client)
        self._input_screen.load_requested.connect(self._on_load_client)

    def _connect_dashboard(self):
        ds = self._dashboard_screen
        ds.mode_changed.connect(self._on_mode_change)
        ds.rotation_changed.connect(self._on_rotation_change)
        ds.language_changed.connect(self._on_language_change)
        ds.time_adjusted.connect(self._on_time_adjust)
        ds.exit_requested.connect(self._show_input)
        ds.export_report.connect(self._on_export_report)
        ds.save_chart_requested.connect(self._on_save_from_dashboard)
        ds.set_transit_time.connect(lambda: self._open_time_dialog("Transit"))
        ds.set_horary_time.connect(lambda: self._open_time_dialog("Horary"))
        ds.open_options.connect(self._open_options)
        ds.open_forward_check.connect(self._open_forward_check)
        ds.open_ssub_tracker.connect(self._open_ssub_tracker)
        ds.open_degree_hits.connect(self._open_degree_hits)
        ds.open_retro_report.connect(self._open_retro_report)
        ds.open_transit_search.connect(self._open_transit_search)
        ds.open_btr.connect(self._open_btr)
        ds.open_medical.connect(self._open_medical)
        ds.open_intraday.connect(self._open_intraday)
        ds.open_longterm.connect(self._open_longterm)
        ds.open_south_kp.connect(self._open_south_kp)
        ds.dasha_tree.set_generator(self._engine.generate_sub_periods)
        ds.clock_format_changed.connect(self._on_clock_format_changed)

    def _on_launch(self, bd: BirthData, language: str):
        ok, msg = self._input_ctrl.validate_and_parse(bd)
        if not ok:
            QMessageBox.warning(self, "Input Error", msg)
            return
        tf = self._input_screen.time_format_24h()
        self._input_ctrl.save_settings(
            bd, language, self._engine.ayanamsa_name, "Mean", time_format_24h=tf,
        )
        self._engine.apply_settings(self._engine.ayanamsa_name, "Mean", language)
        base_time = parse_smart_dt(bd.datetime_str)
        self._dash_ctrl.initialize(bd, base_time, language)
        self._stack.setCurrentWidget(self._dashboard_screen)
        self._dashboard_screen.set_clock_format_24h(tf)
        self._dashboard_screen.rp_panel.set_use_24_hour_clock(tf)
        self._dashboard_screen.rp_panel.set_compute_fn(self._dash_ctrl.compute_rp)
        self._refresh_dashboard()

    def _show_input(self):
        self._dashboard_screen.rp_panel.stop()
        self._stack.setCurrentWidget(self._input_screen)

    def _on_save_client(self):
        bd = self._input_screen.get_birth_data()
        self._save_birth_data_to_clients(bd)

    def _on_save_from_dashboard(self):
        bd = self._dash_ctrl.birth_data
        if not bd:
            QMessageBox.information(self, "No chart", "Open a chart from the entry screen first.")
            return
        self._save_birth_data_to_clients(bd)

    def _save_birth_data_to_clients(self, bd: BirthData):
        ok, msg = self._input_ctrl.save_client(bd)
        if ok:
            QMessageBox.information(self, "Success", msg)
        else:
            QMessageBox.warning(self, "Already Saved", msg)

    def _on_load_client(self):
        clients = self._input_ctrl.get_all_clients()
        if not clients:
            QMessageBox.information(self, "No Data", "No charts saved yet.")
            return
        dlg = ClientListScreen(clients, self)
        dlg.client_selected.connect(self._on_client_selected)
        dlg.exec()

    def _on_client_selected(self, client):
        bd = BirthData(
            name=client.name, dob=client.dob, tob=client.tob, city=client.city,
            latitude=float(client.latitude or 0), longitude=float(client.longitude or 0),
            timezone=client.timezone, horary_number=int(client.horary or 1),
        )
        self._input_screen.set_birth_data(bd)

    def _on_mode_change(self, mode: str):
        self._dash_ctrl.set_mode(mode)
        self._refresh_dashboard()

    def _on_rotation_change(self, rot: int):
        self._dash_ctrl.set_rotation(rot)
        self._refresh_dashboard()

    def _on_language_change(self, lang: str):
        self._engine.set_language(lang)
        self._refresh_dashboard()

    def _on_time_adjust(self, seconds: int):
        self._dash_ctrl.adjust_time(seconds)
        self._refresh_dashboard()

    def _on_clock_format_changed(self, use_24: bool):
        self._settings.update_key("time_format_24h", use_24)
        self._dashboard_screen.rp_panel.set_use_24_hour_clock(use_24)
        bd = self._dash_ctrl.birth_data
        if bd:
            self._dashboard_screen.update_birth_summary(bd, use_24)
        self._refresh_dashboard()

    def _refresh_dashboard(self):
        result = self._dash_ctrl.compute()
        if not result:
            return
        ds = self._dashboard_screen
        ds.lagna_canvas.set_chart(result["lagna_chart"])
        ds.chalit_canvas.set_chart(result["chalit_chart"])
        ds.planet_table.load_rows(result["report_planets"])
        ds.cusp_table.load_rows(result["report_cusps"])
        ds.nadi_widget.load_data(result["report_nadi"], result["report_cusps"])
        ds.dasha_tree.load_mahadashas(result["dasha_nodes"])
        bd = self._dash_ctrl.birth_data
        if bd:
            ds.update_birth_summary(bd)
        from astro_sahayogi.utils.time_format import format_local_datetime

        use_24 = bool(self._settings.get("time_format_24h", True))
        ds.rp_panel.set_use_24_hour_clock(use_24)
        ds.rp_panel.set_info_text(
            format_local_datetime(result["current_time"], use_24)
        )

    def _open_time_dialog(self, mode_target):
        dlg = TimeDialog(mode_target, parent=self)
        def on_time(dt):
            if mode_target == "Transit":
                self._dash_ctrl.set_transit_time(dt)
            else:
                self._dash_ctrl.set_horary_time(dt)
            self._dash_ctrl.set_mode(mode_target)
            self._refresh_dashboard()
        dlg.time_set.connect(on_time)
        dlg.exec()

    def _open_options(self):
        dlg = OptionsDialog(self._engine.ayanamsa_name, "Mean", self)
        def on_change(aya, rahu):
            self._engine.set_ayanamsa(aya)
            self._engine.set_rahu_mode(rahu)
            self._refresh_dashboard()
        dlg.settings_changed.connect(on_change)
        dlg.exec()

    def _on_export_report(self):
        r = self._dash_ctrl.last_result
        if not r:
            QMessageBox.warning(self, "Wait", "Generate a chart first.")
            return
        bd = self._dash_ctrl.birth_data
        if not bd:
            QMessageBox.warning(self, "Wait", "No birth data loaded.")
            return
        try:
            natal = self._dash_ctrl.snapshot_mode("Natal")
            transit = self._dash_ctrl.snapshot_mode("Transit")
            if not natal or not transit:
                QMessageBox.warning(self, "Wait", "Could not build export data.")
                return
            from astro_sahayogi.ui.widgets.chart_canvas import chart_render_data_to_svg
            from astro_sahayogi.services.export.report_helpers import rows_to_table_body
            from astro_sahayogi.services.export.dasha_export import dasha_nodes_to_html

            i18n = self._engine.i18n
            t = i18n.t
            rot = self._dashboard_screen.rotate_combo.currentText()
            mode_disp = t("Natal")
            alt_title = t("Transit")
            active = next((n for n in natal["dasha_nodes"] if n.is_active), None)
            running = (
                f"{t('Active Mahadasha:')} {active.lord_name}" if active else ""
            )

            self._export_ctrl.export_master_report(
                name=bd.name,
                dob=bd.dob,
                tob=bd.tob,
                city=bd.city,
                lat=bd.latitude,
                lon=bd.longitude,
                tz=bd.timezone,
                horary=bd.horary_number,
                mode_display=mode_disp,
                rot_display=rot,
                mode_date_info="",
                lagna_svg=chart_render_data_to_svg(natal["lagna_chart"]),
                chalit_svg=chart_render_data_to_svg(natal["chalit_chart"]),
                lk_block="",
                planets_html=rows_to_table_body(natal["report_planets"]),
                cusps_html=rows_to_table_body(natal["report_cusps"]),
                alt_title=alt_title,
                alt_planets_html=rows_to_table_body(transit["report_planets"]),
                alt_cusps_html=rows_to_table_body(transit["report_cusps"]),
                dasha_html=dasha_nodes_to_html(natal["dasha_nodes"], max_level=2),
                balance_str=natal.get("dasha_balance_str", ""),
                running_dasha=running,
                vastu_html="",
                t=t,
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Report failed",
                f"The report could not be generated:\n\n{e!s}",
            )

    def _open_forward_check(self):
        bd = self._dash_ctrl.birth_data
        dlg = ForwardCheckDialog(bd.timezone, self._engine.ayanamsa_name, self._engine.planet_map, self)
        dlg.exec()

    def _open_ssub_tracker(self):
        bd = self._dash_ctrl.birth_data
        dlg = SSubTrackerDialog(bd.timezone, self._engine.ayanamsa_name, self._engine.planet_map, self._engine.i18n.language, self)
        dlg.exec()

    def _open_degree_hits(self):
        r = self._dash_ctrl.last_result
        if not r:
            return
        dlg = DegreeHitsDialog(r["hit_data_p2p"], r["hit_data_p2h"], self)
        dlg.exec()

    def _open_retro_report(self):
        dlg = RetroReportDialog(self._engine.ayanamsa_name, self._engine.planet_map, self)
        dlg.exec()

    def _open_transit_search(self):
        bd = self._dash_ctrl.birth_data
        dlg = TransitSearchDialog(bd.timezone, self._engine.ayanamsa_name, self._engine.planet_map, self)
        dlg.exec()

    def _open_btr(self):
        bd = self._dash_ctrl.birth_data
        dlg = BTRDialog(bd, bd.timezone, bd.latitude, bd.longitude, self._engine.ayanamsa_name, self._engine.planet_map, self._engine.i18n, self)
        dlg.exec()

    def _open_medical(self):
        r = self._dash_ctrl.last_result
        if not r:
            return
        bd = self._dash_ctrl.birth_data
        dlg = MedicalDialog(r["cusps"], r["planet_data"], bd.timezone, bd.latitude, bd.longitude, self._engine.ayanamsa_name, self._engine.i18n, self)
        dlg.exec()

    def _open_intraday(self):
        r = self._dash_ctrl.last_result
        if not r:
            return
        bd = self._dash_ctrl.birth_data
        dlg = IntradayDialog(r["cusps"], bd.timezone, self._engine.ayanamsa_name, self._engine.i18n, self)
        dlg.exec()

    def _open_longterm(self):
        r = self._dash_ctrl.last_result
        if not r:
            return
        bd = self._dash_ctrl.birth_data
        dlg = LongtermDialog(r["cusps"], bd.timezone, self._engine.ayanamsa_name, self._engine.i18n, self)
        dlg.exec()

    def _open_south_kp(self):
        r = self._dash_ctrl.last_result
        if not r:
            return
        dlg = SouthKPDialog(r["planet_data"], r["cusps"], r["chalit_signs"], r["report_cusps"], self._engine.i18n, self)
        dlg.exec()
