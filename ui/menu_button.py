from PySide6.QtCore import Qt, QSize, QByteArray
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QPushButton

from config import ICONS_DIR


class MenuButton(QPushButton):
    def __init__(self, icon: str, text: str):
        super().__init__(text)
        self.setObjectName("menuButton")
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(48)
        self.setCheckable(True)
        self.setIconSize(QSize(21, 21))

        icon_path = ICONS_DIR / icon
        if icon_path.exists():
            self.setIcon(self._build_icon(icon_path))

    @staticmethod
    def _render_svg(svg: str) -> QPixmap:
        pixmap = QPixmap(42, 42)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer = QSvgRenderer(QByteArray(svg.encode("utf-8")))
        renderer.render(painter)
        painter.end()
        return pixmap

    @classmethod
    def _build_icon(cls, path):
        svg = path.read_text(encoding="utf-8")
        active = svg.replace("#aeb7c3", "#4a8cff")
        icon = QIcon()
        icon.addPixmap(cls._render_svg(svg), QIcon.Normal, QIcon.Off)
        icon.addPixmap(cls._render_svg(active), QIcon.Normal, QIcon.On)
        return icon
