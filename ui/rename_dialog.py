from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)


class RenameDialog(QDialog):

    def __init__(self, name):

        super().__init__()

        self.setWindowTitle(
            "Rename"
        )

        self.resize(420, 170)

        layout = QVBoxLayout(self)

        self.edit = QLineEdit(name)

        layout.addWidget(
            self.edit
        )

        layout.addStretch()

        buttons = QHBoxLayout()

        buttons.addStretch()

        cancel = QPushButton(
            "Cancel"
        )

        rename = QPushButton(
            "Rename"
        )

        buttons.addWidget(cancel)
        buttons.addWidget(rename)

        layout.addLayout(buttons)

        rename.clicked.connect(
            self.accept
        )

        cancel.clicked.connect(
            self.reject
        )

    def value(self):

        return self.edit.text().strip()
