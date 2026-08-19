from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit


class SearchBox(QFrame):
    textChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("searchBox")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 4, 14, 4)
        layout.setSpacing(10)

        icon = QLabel("⌕")
        icon.setObjectName("searchIcon")
        layout.addWidget(icon)

        self.edit = QLineEdit()
        self.edit.setObjectName("searchInput")
        self.edit.setPlaceholderText("Поиск файлов и папок")
        self.edit.setFrame(False)
        self.edit.textChanged.connect(self.textChanged.emit)
        layout.addWidget(self.edit, 1)

        hint = QLabel("Ctrl + F")
        hint.setObjectName("searchHint")
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint)

    def text(self):
        return self.edit.text()

    def clear(self):
        self.edit.clear()

    def setFocus(self):
        self.edit.setFocus()

    def selectAll(self):
        self.edit.selectAll()
