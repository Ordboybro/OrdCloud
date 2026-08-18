from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt


class IconButton(QPushButton):

    def __init__(self, icon: str):
        super().__init__(icon)

        self.setObjectName("iconButton")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(42, 42)
