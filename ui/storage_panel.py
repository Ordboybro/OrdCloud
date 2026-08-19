from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton

from ui.storage_segment import StorageSegment
from ui.storage_stats import StorageStats


class StoragePanel(QFrame):
    upgradeRequested = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("storagePanel")
        self.setMinimumHeight(454)
        self.setMaximumHeight(454)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 16, 4, 16)
        layout.setSpacing(6)

        title = QLabel("Хранилище")
        title.setObjectName("sectionTitle")
        title.setContentsMargins(12, 0, 0, 0)
        layout.addWidget(title)

        self.circle = StorageSegment()
        layout.addWidget(self.circle, alignment=Qt.AlignCenter)

        self.stats = StorageStats()
        layout.addWidget(self.stats)

        upgrade = QPushButton("Увеличить объём")
        upgrade.setObjectName("upgradeButton")
        upgrade.setMinimumHeight(42)
        upgrade.setCursor(Qt.PointingHandCursor)
        upgrade.clicked.connect(self.upgradeRequested.emit)
        layout.addWidget(upgrade)

    def refresh(self):
        self.stats.refresh()
        self.circle.update()
