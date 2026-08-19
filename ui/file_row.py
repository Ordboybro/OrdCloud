from datetime import datetime
from pathlib import Path

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel
from PySide6.QtCore import Signal, Qt

from ui.file_type_icon import FileTypeIcon


class FileRow(QFrame):
    opened = Signal(str)
    selected = Signal(dict)
    contextRequested = Signal(dict)

    def __init__(self, data: dict):
        super().__init__()
        self.data = data
        self.setObjectName("fileRow")
        self.setMinimumHeight(58)
        self.setMaximumHeight(62)
        self.setCursor(Qt.PointingHandCursor)
        self._compact = False
        self._selected = False

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 16, 6)
        layout.setSpacing(14)

        self.icon = FileTypeIcon(Path(data["path"]))
        self.name = QLabel(data["name"])
        self.name.setObjectName("fileName")
        self.modified = QLabel(self._format_date(data.get("modified", "")))
        self.modified.setObjectName("fileDate")
        self.size = QLabel(data.get("size", "—"))
        self.size.setObjectName("fileSize")

        layout.addWidget(self.icon)
        layout.addWidget(self.name, 1)
        layout.addWidget(self.modified)
        layout.addSpacing(25)
        layout.addWidget(self.size)

        self._layout = layout

    @staticmethod
    def _format_date(value):
        if not value:
            return ""
        try:
            return datetime.fromtimestamp(float(value)).strftime("%d.%m.%Y %H:%M")
        except (TypeError, ValueError, OSError):
            return str(value)

    def set_selected(self, value: bool):
        self._selected = value
        self.setProperty("selected", "true" if value else "false")
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def set_compact(self, value: bool):
        self._compact = value
        height = 50 if value else 58
        self.setMinimumHeight(height)
        self.setMaximumHeight(height + 4)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            path = self.data["path"]
            if self.data.get("dir"):
                self.opened.emit(path)
            else:
                try:
                    import os
                    os.startfile(path)
                except OSError:
                    pass
        super().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.selected.emit(self.data)
        elif event.button() == Qt.RightButton:
            self.selected.emit(self.data)
            self.contextRequested.emit(self.data)
        super().mousePressEvent(event)
