from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt

from ui.storage_segment import StorageSegment
from ui.storage_stats import StorageStats


class StoragePanel(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "storagePanel"
        )

        layout = QVBoxLayout(self)

        title = QLabel("Storage")
        title.setObjectName(
            "sectionTitle"
        )

        layout.addWidget(title)

        circle = StorageSegment()

        layout.addWidget(
            circle,
            alignment=Qt.AlignCenter,
        )

        layout.addWidget(
            StorageStats()
        )

        layout.addStretch()
