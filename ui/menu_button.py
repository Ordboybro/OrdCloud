from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton

from config import ICONS_DIR


class MenuButton(QPushButton):
    def __init__(self, icon: str, text: str):
        super().__init__(text)
        self.setObjectName("menuButton")
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(48)
        self.setCheckable(True)
        self.setIconSize(Qt.QSize(21, 21))

        icon_path = ICONS_DIR / icon
        if icon_path.exists():
            self.setIcon(QIcon(str(icon_path)))

