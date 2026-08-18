from pathlib import Path

from PySide6.QtWidgets import *
from PySide6.QtCore import Signal


class Navigation(QWidget):

    pathClicked = Signal(str)

    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout(self)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)

    def setPath(self, path):

        while self.layout.count():

            item = self.layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        path = Path(path)

        home = QPushButton("⌂")

        home.clicked.connect(
            lambda: self.pathClicked.emit(
                str(Path.home())
            )
        )

        self.layout.addWidget(home)

        parts = path.parts

        current = Path(parts[0])

        for part in parts[1:]:

            separator = QLabel("›")

            self.layout.addWidget(separator)

            current /= part

            button = QPushButton(part)

            folder = str(current)

            button.clicked.connect(
                lambda checked=False,
                folder=folder:
                self.pathClicked.emit(folder)
            )

            self.layout.addWidget(button)

        self.layout.addStretch()
