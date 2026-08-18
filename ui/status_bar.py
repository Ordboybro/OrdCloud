from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel


class StatusBar(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("statusBar")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 3, 12, 3)

        self.left = QLabel("0 элементов")
        self.right = QLabel("Готово")

        layout.addWidget(self.left)
        layout.addStretch()
        layout.addWidget(self.right)

    def updateItems(self, count: int):
        word = "элемент" if count == 1 else "элемента" if 2 <= count <= 4 else "элементов"
        self.left.setText(f"{count} {word}")

    def updateStatus(self, text: str):
        self.right.setText(text)
