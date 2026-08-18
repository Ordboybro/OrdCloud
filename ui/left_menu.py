from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Signal

from config import MAX_STORAGE_BYTES
from modules.storage_service import storage
from ui.menu_button import MenuButton


class LeftMenu(QFrame):
    pageChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("leftMenu")
        self.setFixedWidth(205)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 15)
        layout.setSpacing(1)

        logo = QLabel("ORDCLOUD")
        logo.setObjectName("logo")
        layout.addWidget(logo)
        layout.addSpacing(24)

        self.buttons = {}
        self._add_button(layout, "home", "⌂", "Home")
        layout.addSpacing(12)
        self._add_section(layout, "Files")
        self._add_button(layout, "files", "▰", "My Files")
        self._add_button(layout, "documents", "▤", "Documents")
        self._add_button(layout, "images", "▧", "Photo")
        self._add_button(layout, "videos", "▷", "Video")
        self._add_button(layout, "music", "♫", "Music")
        self._add_button(layout, "archives", "▥", "Archives")
        layout.addSpacing(12)
        self._add_section(layout, "Other")
        self._add_button(layout, "trash", "♧", "Trash")

        layout.addStretch(1)

        settings = MenuButton("⚙", "Settings")
        self.buttons["settings"] = settings
        settings.clicked.connect(lambda: self.pageChanged.emit("settings"))
        layout.addWidget(settings)

        storage_label = QLabel("Used 0 B of 5 GB")
        storage_label.setObjectName("storageLabel")
        layout.addWidget(storage_label)

        progress = QProgressBar()
        progress.setObjectName("storageProgress")
        progress.setRange(0, 100)
        progress.setValue(0)
        progress.setTextVisible(False)
        layout.addWidget(progress)

        self.storage_label = storage_label
        self.storage_progress = progress
        self.refresh_storage()
        self.select("home")

    def _add_section(self, layout, text):
        label = QLabel(text)
        label.setObjectName("menuSection")
        layout.addWidget(label)

    def _add_button(self, layout, key, icon, text):
        button = MenuButton(icon, text)
        self.buttons[key] = button
        layout.addWidget(button)
        button.clicked.connect(lambda checked=False, k=key: self.select(k))

    def select(self, key: str):
        for name, button in self.buttons.items():
            button.setChecked(name == key)
        self.pageChanged.emit(key)

    def refresh_storage(self):
        try:
            used = storage.get_size()
        except Exception:
            used = 0
        percent = min(100, int(used / MAX_STORAGE_BYTES * 100)) if MAX_STORAGE_BYTES else 0
        self.storage_progress.setValue(percent)
        self.storage_label.setText(f"Used {self._format_size(used)} of 5 GB")

    @staticmethod
    def _format_size(size):
        if size < 1024:
            return f"{size} B"
        if size < 1024 ** 2:
            return f"{size / 1024:.1f} KB"
        if size < 1024 ** 3:
            return f"{size / 1024 ** 2:.1f} MB"
        return f"{size / 1024 ** 3:.1f} GB"
