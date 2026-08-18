import sys

from PySide6.QtWidgets import QApplication

from config import APP_NAME, THEME
from ui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)

    if THEME.exists():
        THEME_CONTENT = THEME.read_text(encoding="utf-8")
        app.setStyleSheet(THEME_CONTENT)

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
