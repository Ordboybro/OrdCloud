from PySide6.QtWidgets import *
from PySide6.QtCore import Signal


class SearchBox(QFrame):

    textChanged = Signal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("searchBox")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 4, 12, 4)

        icon = QLabel("⌕")

        self.edit = QLineEdit()

        self.edit.setPlaceholderText(
            "Search files..."
        )

        self.edit.textChanged.connect(
            self.textChanged.emit
        )

        layout.addWidget(icon)
        layout.addWidget(self.edit)

    def text(self):
        return self.edit.text()
