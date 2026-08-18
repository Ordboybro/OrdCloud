from PySide6.QtWidgets import *


class ActionBar(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("actionBar")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)

        actions = [
            "＋ New Folder",
            "↑ Upload",
            "Copy",
            "Paste",
            "Rename",
            "Delete",
        ]

        self.buttons = {}

        for text in actions:

            button = QPushButton(text)

            self.buttons[text] = button

            layout.addWidget(button)

        layout.addStretch()
