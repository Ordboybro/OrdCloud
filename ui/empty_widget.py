from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt


class EmptyWidget(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "emptyWidget"
        )

        layout = QVBoxLayout(self)

        layout.addStretch()

        icon = QLabel("📂")
        icon.setObjectName(
            "emptyIcon"
        )

        text = QLabel(
            "Folder is empty"
        )
        text.setObjectName(
            "emptyText"
        )

        icon.setAlignment(
            Qt.AlignCenter
        )

        text.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(icon)
        layout.addWidget(text)

        layout.addStretch()
