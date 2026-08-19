from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit

from config import ICONS_DIR


class SearchBox(QFrame):
    textChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("searchBox")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 4, 14, 4)
        layout.setSpacing(10)

        icon = QLabel()
        icon.setObjectName("searchIcon")
        icon.setFixedSize(22, 22)
        icon.setPixmap(QIcon(str(ICONS_DIR / "ui_search.svg")).pixmap(QSize(22, 22)))
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
