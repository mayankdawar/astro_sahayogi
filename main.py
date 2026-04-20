"""Astro Sahayogi entry point."""
import sys
import os
import types


def configure_import_paths() -> None:
    """Make package imports stable even if project folder name changes."""
    project_root = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(project_root)
    package_name = "astro_sahayogi"

    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # If folder name is not "astro_sahayogi" (e.g. GitHub zip extraction),
    # create a runtime package alias so absolute imports still resolve.
    if package_name not in sys.modules:
        package = types.ModuleType(package_name)
        package.__path__ = [project_root]
        sys.modules[package_name] = package


configure_import_paths()

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QTextStream

from astro_sahayogi.app import AstroSahayogiApp
from astro_sahayogi.ui.screens.splash_screen import SplashScreen


def load_theme(app: QApplication):
    theme_path = os.path.join(os.path.dirname(__file__), "ui", "theme", "astro_theme.qss")
    if os.path.exists(theme_path):
        with open(theme_path, "r") as f:
            app.setStyleSheet(f.read())


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Astro Sahayogi")
    app.setOrganizationName("AstroSahayogi")
    load_theme(app)

    splash = SplashScreen()
    splash.show()

    main_window = AstroSahayogiApp()

    def on_ready():
        splash.close()
        main_window.show()

    splash.ready.connect(on_ready)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
