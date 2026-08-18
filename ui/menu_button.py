from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt


class MenuButton(QPushButton):

    def __init__(self, icon: str, text: str):
        super().__init__(f"{icon}  {text}")

        self.setObjectName("menuButton")
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(46)
        self.setCheckable(True)
