from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel
from PySide6.QtCore import Signal, Qt


class FileRow(QFrame):

    opened = Signal(str)
    selected = Signal(dict)

    def __init__(self, data: dict):
        super().__init__()

        self.data = data

        self.setObjectName("fileRow")
        self.setMinimumHeight(52)
        self.setMaximumHeight(58)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            12,
            4,
            12,
            4,
        )

        layout.setSpacing(12)

        self.icon = QLabel(
            data.get("icon", "📄")
        )

        self.icon.setObjectName(
            "fileIcon"
        )

        self.name = QLabel(
            data["name"]
        )

        self.name.setObjectName(
            "fileName"
        )

        self.modified = QLabel(
            data.get("modified", "")
        )

        self.modified.setObjectName(
            "fileDate"
        )

        self.size = QLabel(
            data.get("size", "—")
        )

        self.size.setObjectName(
            "fileSize"
        )

        layout.addWidget(
            self.icon
        )

        layout.addWidget(
            self.name,
            1,
        )

        layout.addWidget(
            self.modified
        )

        layout.addSpacing(25)

        layout.addWidget(
            self.size
        )

        self.setCursor(
            Qt.PointingHandCursor
        )

    def mouseDoubleClickEvent(self, event):

        if self.data.get("dir"):

            self.opened.emit(
                self.data["path"]
            )

        super().mouseDoubleClickEvent(
            event
        )

    def mousePressEvent(self, event):

        self.selected.emit(
            self.data
        )

        super().mousePressEvent(
            event
        )
