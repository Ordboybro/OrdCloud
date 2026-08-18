from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtCore import Qt

from config import MAX_STORAGE_BYTES
from modules.storage_service import storage
from ui.storage_stats import StorageStats


class StorageSegment(QWidget):
    COLORS = ("#5F89FF", "#6ED0A9", "#FFB84D", "#FF6A7A")

    def __init__(self):
        super().__init__()
        self.setMinimumSize(230, 230)
        self.setMaximumHeight(230)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(22, 22, -22, -22)
        sizes = StorageStats._sizes()
        values = [sizes[name] for name, _, _ in StorageStats.CATEGORIES]
        total = sum(values)

        if total == 0:
            pen = QPen(QColor("#2A3442"), 17)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            painter.drawArc(rect, -90 * 16, 360 * 16)
        else:
            start = -90 * 16
            for index, value in enumerate(values):
                if value <= 0:
                    continue
                angle = int(value / total * 360 * 16)
                pen = QPen(QColor(self.COLORS[index]), 17)
                pen.setCapStyle(Qt.RoundCap)
                painter.setPen(pen)
                painter.drawArc(rect, start, -angle)
                start -= angle

        used = storage.get_size()
        used_gb = used / 1024 ** 3

        painter.setPen(QColor("#FFFFFF"))
        font = QFont("Segoe UI", 22)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(self.rect().adjusted(0, -6, 0, -6), Qt.AlignCenter, f"{used_gb:.1f} GB")

        painter.setPen(QColor("#788499"))
        small = QFont("Segoe UI", 9)
        painter.setFont(small)
        painter.drawText(self.rect().adjusted(0, 27, 0, 27), Qt.AlignCenter, f"of {MAX_STORAGE_BYTES / 1024 ** 3:.0f} GB")
