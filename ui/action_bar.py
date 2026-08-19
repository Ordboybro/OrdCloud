from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt


class ActionBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("actionBar")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(2)

        actions = [
            ("new_folder", "+  Новая папка"),
            ("upload", "↑  Загрузить"),
            ("copy", "Копировать"),
            ("paste", "Вставить"),
            ("rename", "Переименовать"),
            ("delete", "Удалить"),
        ]

        self.buttons = {}
        for key, text in actions:
            button = QPushButton(text)
            button.setCursor(Qt.PointingHandCursor)
            button.setProperty("actionKey", key)
            self.buttons[key] = button
            layout.addWidget(button)

        self.new_folder = self.buttons["new_folder"]
        self.upload = self.buttons["upload"]
        self.copy = self.buttons["copy"]
        self.paste = self.buttons["paste"]
        self.rename = self.buttons["rename"]
        self.delete = self.buttons["delete"]
        layout.addStretch()
