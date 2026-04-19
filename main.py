"""Astro Sahayogi entry point."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
