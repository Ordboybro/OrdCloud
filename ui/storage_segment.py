from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtCore import Qt


class StorageSegment(QWidget):

    def __init__(self):
        super().__init__()

        self.setMinimumSize(250, 250)

        self.parts = [
            ("#5F89FF", 45),
            ("#6ED0A9", 25),
            ("#FFB84D", 18),
            ("#FF6A7A", 12),
        ]

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        rect = self.rect().adjusted(
            28, 28, -28, -28
        )

        start = -90 * 16

        for color, value in self.parts:

            pen = QPen(
                QColor(color),
                18,
            )

            pen.setCapStyle(
                Qt.RoundCap
            )

            painter.setPen(pen)

            angle = int(
                -value * 360 * 16 / 100
            )

            painter.drawArc(
                rect,
                start,
                angle,
            )

            start += angle

        painter.setPen(
            QColor("#FFFFFF")
        )

        font = QFont()
        font.setPointSize(23)
        font.setBold(True)

        painter.setFont(font)

        painter.drawText(
            self.rect(),
            Qt.AlignCenter,
            "4.8 GB",
        )
