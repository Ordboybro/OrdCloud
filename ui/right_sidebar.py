from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget

from config import ICONS_DIR
from ui.storage_panel import StoragePanel


class RightSidebar(QFrame):
    uploadRequested = Signal()
    upgradeRequested = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("rightSidebar")
        self.setFixedWidth(286)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 104, 32, 28)
        layout.setSpacing(14)

        self.storage = StoragePanel()
        self.storage.upgradeRequested.connect(self.upgradeRequested.emit)
        layout.addWidget(self.storage)

        upload_container = QWidget()
        upload_layout = QVBoxLayout(upload_container)
        upload_layout.setContentsMargins(18, 0, 0, 0)
        upload_layout.setSpacing(10)

        upload_title = QLabel("Загрузить файлы")
        upload_title.setObjectName("uploadTitle")
        upload_layout.addWidget(upload_title)

        self.upload_box = QFrame()
        self.upload_box.setObjectName("uploadBox")
        self.upload_box.setCursor(Qt.PointingHandCursor)
        box_layout = QVBoxLayout(self.upload_box)
        box_layout.setContentsMargins(12, 16, 12, 16)
        box_layout.setSpacing(5)

        icon = QLabel()
        icon.setObjectName("uploadIcon")
        icon.setAlignment(Qt.AlignCenter)
        icon.setPixmap(QIcon(str(ICONS_DIR / "ui_upload.svg")).pixmap(QSize(40, 40)))
        text = QLabel("Перетащите файлы сюда")
        text.setObjectName("uploadText")
        text.setAlignment(Qt.AlignCenter)
        hint = QLabel("или нажмите для выбора")
        hint.setObjectName("uploadHint")
        hint.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(icon)
        box_layout.addWidget(text)
        box_layout.addWidget(hint)
        self.upload_box.mousePressEvent = self._browse
        upload_layout.addWidget(self.upload_box)
        layout.addWidget(upload_container)
        layout.addStretch(1)

    def _browse(self, event):
        if event.button() == Qt.LeftButton:
            self.uploadRequested.emit()

    def refresh(self):
        self.storage.refresh()
