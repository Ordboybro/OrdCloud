from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QWidget


class FileTypeIcon(QWidget):
    """Small painted file icon used by the dashboard without external thumbnails."""

    def __init__(self, path: Path):
        super().__init__()
        self.path = Path(path)
        self.setFixedSize(42, 42)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect().adjusted(1, 1, -1, -1)
        ext = self.path.suffix.lower()

        if self.path.is_dir():
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor("#3477e9"))
            painter.drawRoundedRect(rect.adjusted(2, 7, -2, -3), 7, 7)
            painter.drawRoundedRect(rect.adjusted(5, 4, -17, -22), 4, 4)
            return

        colors = {
            ".pdf": ("#d8423b", "PDF"),
            ".doc": ("#2f73d8", "W"),
            ".docx": ("#2f73d8", "W"),
            ".xls": ("#2f9b60", "X"),
            ".xlsx": ("#2f9b60", "X"),
            ".zip": ("#8b55c7", "↕"),
            ".rar": ("#8b55c7", "↕"),
        }

        if ext in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor("#4d83b8"))
            painter.drawRoundedRect(rect, 7, 7)
            painter.setBrush(QColor("#d7e6f7"))
            painter.drawEllipse(11, 10, 7, 7)
            painter.setBrush(QColor("#8fc28f"))
            painter.drawPolygon([(6, 34), (16, 24), (23, 30), (29, 23), (38, 34)])
            return

        color, glyph = colors.get(ext, ("#536170", "•"))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(color))
        painter.drawRoundedRect(rect, 7, 7)
        painter.setPen(QPen(QColor("#ffffff")))
        font = QFont("Segoe UI", 13 if glyph == "PDF" else 20)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, glyph)
