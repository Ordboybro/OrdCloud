from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel

from modules.storage_service import storage


class StorageStats(QFrame):
    CATEGORIES = (
        ("Документы", "#5F89FF"),
        ("Изображения", "#6ED0A9"),
        ("Видео", "#FFB84D"),
        ("Другое", "#FF6A7A"),
    )

    def __init__(self):
        super().__init__()
        self.setObjectName("storageStats")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 8, 12, 8)
        self.layout.setSpacing(6)
        self.refresh()

    @staticmethod
    def _format_size(size):
        if size < 1024:
            return f"{size} Б"
        if size < 1024 ** 2:
            return f"{size / 1024:.1f} КБ"
        if size < 1024 ** 3:
            return f"{size / 1024 ** 2:.1f} МБ"
        return f"{size / 1024 ** 3:.1f} ГБ"

    def refresh(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        sizes = storage.get_snapshot()["categories"]
        for title, color in self.CATEGORIES:
            row = QHBoxLayout()
            dot = QLabel("●")
            dot.setStyleSheet(f"color: {color};")
            label = QLabel(title)
            value = QLabel(self._format_size(sizes[title]))
            row.addWidget(dot)
            row.addWidget(label)
            row.addStretch()
            row.addWidget(value)
            self.layout.addLayout(row)
