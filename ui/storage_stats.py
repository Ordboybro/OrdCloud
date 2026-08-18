from pathlib import Path

from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel

from modules.storage_service import storage_path


class StorageStats(QFrame):

    CATEGORIES = (
        ("Documents", "#5F89FF", {".txt", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".csv", ".py", ".json", ".md"}),
        ("Images", "#6ED0A9", {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg"}),
        ("Videos", "#FFB84D", {".mp4", ".mkv", ".avi", ".mov", ".webm"}),
        ("Other", "#FF6A7A", set()),
    )

    def __init__(self):
        super().__init__()
        self.setObjectName("storageStats")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 10, 12, 10)
        self.refresh()

    @staticmethod
    def _format_size(size):
        if size < 1024:
            return f"{size} B"
        if size < 1024 ** 2:
            return f"{size / 1024:.1f} KB"
        if size < 1024 ** 3:
            return f"{size / 1024 ** 2:.1f} MB"
        return f"{size / 1024 ** 3:.1f} GB"

    @classmethod
    def _sizes(cls):
        sizes = {name: 0 for name, _, _ in cls.CATEGORIES}
        extensions = {}
        for name, _, exts in cls.CATEGORIES:
            for ext in exts:
                extensions[ext] = name

        root = storage_path()
        try:
            for path in root.rglob("*"):
                if not path.is_file():
                    continue
                category = extensions.get(path.suffix.lower(), "Other")
                try:
                    sizes[category] += path.stat().st_size
                except OSError:
                    continue
        except OSError:
            pass

        return sizes

    def refresh(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        sizes = self._sizes()

        for title, color, _ in self.CATEGORIES:
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
