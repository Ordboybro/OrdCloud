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
        self.setFixedWidth(332)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 20, 28)
        layout.setSpacing(2)
        self.buttons = {}

        self._add_button(layout, "home", "ui_home.svg", "Главная")
        self._add_button(layout, "recent", "ui_recent.svg", "Недавние")
        self._add_button(layout, "favorites", "ui_star.svg", "Помеченные")

        layout.addSpacing(17)
        self._add_section(layout, "Файлы")
        self._add_button(layout, "files", "ui_folder.svg", "Все файлы")
        self._add_button(layout, "documents", "ui_document.svg", "Документы")
        self._add_button(layout, "images", "ui_image.svg", "Фото")
        self._add_button(layout, "videos", "ui_video.svg", "Видео")
        self._add_button(layout, "music", "ui_music.svg", "Музыка")
        self._add_button(layout, "archives", "ui_archive.svg", "Архивы")

        layout.addSpacing(17)
        self._add_section(layout, "Другое")
        self._add_button(layout, "trash", "ui_trash.svg", "Корзина")

        layout.addStretch(1)

        settings = MenuButton("ui_settings.svg", "Настройки")
        self.buttons["settings"] = settings
        settings.clicked.connect(lambda: self.pageChanged.emit("settings"))
        layout.addWidget(settings)

        storage_label = QLabel("Использовано 0 ГБ из 5 ГБ")
        storage_label.setObjectName("storageLabel")
        layout.addWidget(storage_label)

        progress = QProgressBar()
        progress.setObjectName("storageProgress")
        progress.setRange(0, 100)
        progress.setValue(0)
        progress.setTextVisible(False)
        layout.addWidget(progress)

        percent_label = QLabel("0%")
        percent_label.setObjectName("storagePercent")
        percent_label.setAlignment(Qt.AlignRight)
        layout.addWidget(percent_label)

        self.storage_label = storage_label
        self.storage_progress = progress
        self.storage_percent = percent_label
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
        self.storage_percent.setText(f"{percent}%")

    @staticmethod
    def _format_size(size):
        if size < 1024:
            return f"{size} Б"
        if size < 1024 ** 2:
            return f"{size / 1024:.1f} КБ"
        if size < 1024 ** 3:
            return f"{size / 1024 ** 2:.1f} МБ"
        return f"{size / 1024 ** 3:.1f} ГБ"
