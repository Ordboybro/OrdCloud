import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from config import APP_NAME, THEME
from ui.main_window import MainWindow


def main() -> int:
    # Keep Qt rendering crisp on high-DPI displays while preserving the reference layout.
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName("Ordboybro")
    app.setApplicationDisplayName(APP_NAME)
    app.setStyle("Fusion")

    if THEME.exists():
        app.setStyleSheet(THEME.read_text(encoding="utf-8"))

    window = MainWindow()
    window.show()
    window.raise_()
    window.activateWindow()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
