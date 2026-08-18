from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Signal

from ui.menu_button import MenuButton


class LeftMenu(QFrame):

    pageChanged = Signal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("leftMenu")
        self.setFixedWidth(250)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(6)

        logo = QLabel("ORDCLOUD")
        logo.setObjectName("logo")
        logo.setToolTip("OrdCloud")

        layout.addWidget(logo)
        layout.addSpacing(24)

        self.buttons = {}

        items = [
            ("home", "⌂", "Home"),
            ("files", "□", "My Files"),
            ("favorites", "☆", "Favorites"),
            ("recent", "◷", "Recent"),
            ("cloud", "☁", "Cloud"),
            ("uploads", "↑", "Uploads"),
            ("trash", "⌫", "Trash"),
        ]

        for key, icon, text in items:
            button = MenuButton(icon, text)
            self.buttons[key] = button
            layout.addWidget(button)
            button.clicked.connect(
                lambda checked=False, k=key: self.select(k)
            )

        layout.addStretch()

        settings = MenuButton("⚙", "Settings")
        self.buttons["settings"] = settings
        layout.addWidget(settings)

        self.select("home")

    def select(self, key: str):
        for name, button in self.buttons.items():
            button.setChecked(name == key)

        self.pageChanged.emit(key)
