"""Export controller: manages file dialogs and export service calls."""
from __future__ import annotations
import webbrowser
import os
from PySide6.QtWidgets import QFileDialog, QWidget

from astro_sahayogi.services.export.charts_report import ChartsReportExporter
from astro_sahayogi.services.export.master_report import MasterReportExporter


class ExportController:
    def __init__(self, parent_widget: QWidget):
        self._parent = parent_widget

    def export_charts(self, **kwargs) -> bool:
        name = kwargs.get("name", "chart")
        filepath, _ = QFileDialog.getSaveFileName(
            self._parent, "Save Charts", f"{name}_Charts.html", "HTML Files (*.html)",
        )
        if not filepath:
            return False
        exporter = ChartsReportExporter()
        exporter.export(filepath, **kwargs)
        webbrowser.open("file://" + os.path.realpath(filepath))
        return True

    def export_master_report(self, **kwargs) -> bool:
        name = kwargs.get("name", "report")
        filepath, _ = QFileDialog.getSaveFileName(
            self._parent, "Save Master Report", f"{name}_Master_Report.html", "HTML Files (*.html)",
        )
        if not filepath:
            return False
        exporter = MasterReportExporter()
        exporter.export(filepath, **kwargs)
        webbrowser.open("file://" + os.path.realpath(filepath))
        return True
