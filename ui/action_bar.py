from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton

from config import ICONS_DIR


class ActionBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("actionBar")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(2)

        actions = [
            ("new_folder", "action_new_folder.svg", "Новая папка"),
            ("upload", "ui_upload.svg", "Загрузить"),
            ("copy", "action_copy.svg", "Копировать"),
            ("paste", "action_paste.svg", "Вставить"),
            ("rename", "action_rename.svg", "Переименовать"),
            ("delete", "action_delete.svg", "Удалить"),
        ]

        self.buttons = {}
        for key, icon_name, text in actions:
            button = QPushButton(text)
            button.setCursor(Qt.PointingHandCursor)
            button.setProperty("actionKey", key)
            button.setIcon(QIcon(str(ICONS_DIR / icon_name)))
            button.setIconSize(QSize(18, 18))
            self.buttons[key] = button
            layout.addWidget(button)

        self.new_folder = self.buttons["new_folder"]
        self.upload = self.buttons["upload"]
        self.copy = self.buttons["copy"]
        self.paste = self.buttons["paste"]
        self.rename = self.buttons["rename"]
        self.delete = self.buttons["delete"]
        layout.addStretch()
