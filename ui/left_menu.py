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
        self.setFixedWidth(310)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 24)
        layout.setSpacing(3)
        self.buttons = {}

        self._add_button(layout, "home", "⌂", "Главная")
        self._add_button(layout, "recent", "◷", "Недавние")
        self._add_button(layout, "favorites", "☆", "Помеченные")

        layout.addSpacing(18)
        self._add_section(layout, "Файлы")
        self._add_button(layout, "files", "□", "Все файлы")
        self._add_button(layout, "documents", "▤", "Документы")
        self._add_button(layout, "images", "▧", "Фото")
        self._add_button(layout, "videos", "▷", "Видео")
        self._add_button(layout, "music", "♫", "Музыка")
        self._add_button(layout, "archives", "▥", "Архивы")

        layout.addSpacing(18)
        self._add_section(layout, "Другое")
        self._add_button(layout, "trash", "♜", "Корзина")

        layout.addStretch(1)

        settings = MenuButton("⚙", "Настройки")
        self.buttons["settings"] = settings
        settings.clicked.connect(lambda: self.pageChanged.emit("settings"))
        layout.addWidget(settings)

        storage_label = QLabel("Использовано 0 Б из 5 ГБ")
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
        self.select("home", emit=False)

    def _add_section(self, layout, text):
        label = QLabel(text)
        label.setObjectName("menuSection")
        layout.addWidget(label)

    def _add_button(self, layout, key, icon, text):
        button = MenuButton(icon, text)
        self.buttons[key] = button
        layout.addWidget(button)
        button.clicked.connect(lambda checked=False, k=key: self.select(k))

    def select(self, key: str, emit=True):
        for name, button in self.buttons.items():
            button.setChecked(name == key)
        if emit:
            self.pageChanged.emit(key)

    def refresh_storage(self):
        try:
            used = storage.get_size()
        except OSError:
            used = 0
        percent = min(100, int(used / MAX_STORAGE_BYTES * 100)) if MAX_STORAGE_BYTES else 0
        self.storage_progress.setValue(percent)
        self.storage_label.setText(f"Использовано {self._format_size(used)} из 5 ГБ")

    @staticmethod
    def _format_size(size):
        if size < 1024:
            return f"{size} Б"
        if size < 1024 ** 2:
            return f"{size / 1024:.1f} КБ"
        if size < 1024 ** 3:
            return f"{size / 1024 ** 2:.1f} МБ"
        return f"{size / 1024 ** 3:.1f} ГБ"
