from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtCore import Qt

from config import MAX_STORAGE_BYTES
from modules.storage_service import storage


class StorageSegment(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(245, 245)
        self.setMaximumSize(245, 245)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect().adjusted(18, 18, -18, -18)
        snapshot = storage.get_snapshot()
        used = max(0, snapshot["size"])
        ratio = min(1.0, used / MAX_STORAGE_BYTES) if MAX_STORAGE_BYTES else 0.0
        percent = int(round(ratio * 100))

        track = QPen(QColor("#3b424a"), 18)
        track.setCapStyle(Qt.RoundCap)
        painter.setPen(track)
        painter.drawArc(rect, -90 * 16, 360 * 16)

        if ratio > 0:
            progress = QPen(QColor("#3f82ff"), 18)
            progress.setCapStyle(Qt.RoundCap)
            painter.setPen(progress)
            painter.drawArc(rect, -90 * 16, int(-ratio * 360 * 16))

        painter.setPen(QColor("#f2f4f7"))
        painter.setFont(QFont("Segoe UI", 27))
        painter.drawText(self.rect().adjusted(0, -5, 0, -5), Qt.AlignCenter, f"{percent}%")

        painter.setPen(QColor("#9aa2ad"))
        painter.setFont(QFont("Segoe UI", 11))
        painter.drawText(self.rect().adjusted(0, 34, 0, 34), Qt.AlignCenter, "Использовано")
