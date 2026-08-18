from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)


class StorageStats(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "storageStats"
        )

        layout = QVBoxLayout(self)

        data = [
            ("Documents", "#5F89FF", "2.1 GB"),
            ("Images", "#6ED0A9", "1.2 GB"),
            ("Videos", "#FFB84D", "1.0 GB"),
            ("Other", "#FF6A7A", "0.5 GB"),
        ]

        for title, color, size in data:

            row = QHBoxLayout()

            dot = QLabel("●")

            dot.setStyleSheet(
                f"color: {color};"
            )

            label = QLabel(title)
            value = QLabel(size)

            row.addWidget(dot)
            row.addWidget(label)
            row.addStretch()
            row.addWidget(value)

            layout.addLayout(row)
