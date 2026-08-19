from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton

from config import ICONS_DIR


class IconButton(QPushButton):
    def __init__(self, icon: str):
        super().__init__()
        self.setObjectName("iconButton")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(44, 44)
        self.setIconSize(QSize(22, 22))

        path = ICONS_DIR / icon
        if path.exists():
            self.setIcon(QIcon(str(path)))
        else:
            self.setText(icon)
