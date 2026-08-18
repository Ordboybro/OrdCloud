from PySide6.QtWidgets import *

from ui.storage_panel import StoragePanel


class RightSidebar(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "rightSidebar"
        )

        self.setFixedWidth(330)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            18, 18, 18, 18
        )

        layout.addWidget(
            StoragePanel()
        )

        layout.addStretch()

        upgrade = QPushButton(
            "Upgrade Plan"
        )

        upgrade.setMinimumHeight(46)

        layout.addWidget(upgrade)
