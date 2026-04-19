"""RP controller: provides the compute function to RPPanel."""
from __future__ import annotations
from astro_sahayogi.ui.controllers.dashboard_controller import DashboardController


class RPController:
    def __init__(self, dashboard_ctrl: DashboardController):
        self._ctrl = dashboard_ctrl

    def compute_rp(self) -> dict:
        return self._ctrl.compute_rp()
