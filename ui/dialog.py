from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)


class Dialog(QDialog):

    def __init__(
        self,
        title,
        text,
    ):
        super().__init__()

        self.setWindowTitle(title)
        self.setModal(True)

        self.resize(420, 190)

        layout = QVBoxLayout(self)

        label = QLabel(text)
        label.setWordWrap(True)

        layout.addWidget(label)

        layout.addStretch()

        buttons = QHBoxLayout()

        buttons.addStretch()

        cancel = QPushButton(
            "Cancel"
        )

        ok = QPushButton(
            "OK"
        )

        buttons.addWidget(cancel)
        buttons.addWidget(ok)

        layout.addLayout(buttons)

        cancel.clicked.connect(
            self.reject
        )

        ok.clicked.connect(
            self.accept
        )
