from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit


class SearchBox(QFrame):
    textChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("searchBox")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 4, 12, 4)
        layout.setSpacing(8)

        icon = QLabel("⌕")
        self.edit = QLineEdit()
        self.edit.setObjectName("searchInput")
        self.edit.setPlaceholderText("Search files...")
        self.edit.setFrame(False)
        self.edit.textChanged.connect(self.textChanged.emit)

        layout.addWidget(icon)
        layout.addWidget(self.edit, 1)

    def text(self):
        return self.edit.text()

    def clear(self):
        self.edit.clear()

    def setFocus(self):
        self.edit.setFocus()

    def selectAll(self):
        self.edit.selectAll()
