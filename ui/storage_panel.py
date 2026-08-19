from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

from ui.storage_segment import StorageSegment
from ui.storage_stats import StorageStats


class StoragePanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("storagePanel")
        self.setMinimumHeight(454)
        self.setMaximumHeight(454)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(6)

        title = QLabel("Хранилище")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        self.circle = StorageSegment()
        layout.addWidget(self.circle, alignment=Qt.AlignCenter)

        self.stats = StorageStats()
        layout.addWidget(self.stats)

    def refresh(self):
        self.stats.refresh()
        self.circle.update()
