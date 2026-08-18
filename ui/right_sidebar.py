from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

from ui.storage_panel import StoragePanel


class RightSidebar(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("rightSidebar")
        self.setFixedWidth(320)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        self.storage = StoragePanel()
        layout.addWidget(self.storage)

        upload_title = QLabel("Upload files")
        upload_title.setObjectName("uploadTitle")
        layout.addWidget(upload_title)

        self.upload_box = QFrame()
        self.upload_box.setObjectName("uploadBox")
        upload_layout = QVBoxLayout(self.upload_box)
        upload_layout.setContentsMargins(12, 18, 12, 18)
        upload_layout.setSpacing(6)

        icon = QLabel("⇧")
        icon.setObjectName("uploadIcon")
        icon.setAlignment(Qt.AlignCenter)
        text = QLabel("Drop files here")
        text.setObjectName("uploadText")
        text.setAlignment(Qt.AlignCenter)
        hint = QLabel("or click to browse")
        hint.setObjectName("uploadHint")
        hint.setAlignment(Qt.AlignCenter)
        upload_layout.addWidget(icon)
        upload_layout.addWidget(text)
        upload_layout.addWidget(hint)
        self.upload_box.mousePressEvent = self._browse
        layout.addWidget(self.upload_box)

        layout.addStretch(1)

        upgrade = QPushButton("Upgrade Plan")
        upgrade.setMinimumHeight(42)
        upgrade.setCursor(Qt.PointingHandCursor)
        layout.addWidget(upgrade)

    def _browse(self, event):
        from PySide6.QtWidgets import QFileDialog
        QFileDialog.getOpenFileNames(self, "Upload files")

    def refresh(self):
        self.storage.refresh()
