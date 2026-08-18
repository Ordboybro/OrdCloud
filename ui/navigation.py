from pathlib import Path

from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal

from modules.storage_service import storage_path


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

        root = storage_path().resolve()
        path = Path(path).resolve()
        try:
            relative = path.relative_to(root)
        except ValueError:
            return

        home = QPushButton("⌂")
        home.setToolTip("My Files")
        home.clicked.connect(lambda: self.pathClicked.emit(str(root)))
        self.layout.addWidget(home)

        current = root
        for part in relative.parts:
            self.layout.addWidget(QLabel("›"))
            current = current / part
            button = QPushButton(part)
            folder = str(current)
            button.clicked.connect(lambda checked=False, folder=folder: self.pathClicked.emit(folder))
            self.layout.addWidget(button)

        self.layout.addStretch()
