from pathlib import Path
from datetime import datetime

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from modules.favorites import Favorites
from modules.recent import Recent
from modules.storage_service import storage_path


class QuickCard(QFrame):
    opened = Signal(str)

    def __init__(self, title: str, icon: str, path_name: str, color_name: str):
        super().__init__()
        self.setObjectName("quickCard")
        self.setCursor(Qt.PointingHandCursor)
        self.path_name = path_name
        self.setProperty("cardType", color_name)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)

        icon_label = QLabel(icon)
        icon_label.setObjectName("quickIcon")
        icon_label.setProperty("iconType", color_name)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        text = QVBoxLayout()
        text.setSpacing(1)
        name = QLabel(title)
        name.setObjectName("quickTitle")
        count = QLabel(self._count())
        count.setObjectName("quickCount")
        text.addWidget(name)
        text.addWidget(count)
        layout.addLayout(text, 1)

    def _count(self) -> str:
        folder = storage_path() / self.path_name
        try:
            count = sum(1 for p in folder.iterdir()) if folder.exists() else 0
            return f"{count} files"
        except OSError:
            return "0 files"

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.opened.emit(self.path_name)
        super().mousePressEvent(event)


class RecentRow(QFrame):
    opened = Signal(str)
    favoriteChanged = Signal(str, bool)

    def __init__(self, path: Path, favorites: Favorites):
        super().__init__()
        self.path = path
        self.favorites = favorites
        self.setObjectName("recentRow")
        self.setCursor(Qt.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 3, 8, 3)
        layout.setSpacing(10)

        icon = "▣" if path.is_dir() else "▤"
        icon_label = QLabel(icon)
        icon_label.setObjectName("recentIcon")
        icon_label.setFixedWidth(28)
        layout.addWidget(icon_label)

        name_label = QLabel(path.name)
        name_label.setObjectName("recentName")
        layout.addWidget(name_label, 1)

        try:
            stat = path.stat()
            modified = datetime.fromtimestamp(stat.st_mtime).strftime("%d.%m.%Y %H:%M")
            size = "—" if path.is_dir() else self._format_size(stat.st_size)
        except OSError:
            modified, size = "—", "—"

        date_label = QLabel(modified)
        date_label.setObjectName("recentMeta")
        date_label.setFixedWidth(145)
        layout.addWidget(date_label)

        size_label = QLabel(size)
        size_label.setObjectName("recentMeta")
        size_label.setFixedWidth(70)
        layout.addWidget(size_label)

        self.star = QPushButton("★" if favorites.contains(str(path)) else "☆")
        self.star.setObjectName("recentStar")
        self.star.setFixedSize(28, 28)
        self.star.setCursor(Qt.PointingHandCursor)
        self.star.clicked.connect(self._toggle_favorite)
        layout.addWidget(self.star)

        more = QPushButton("•••")
        more.setObjectName("recentMore")
        more.setFixedSize(30, 28)
        more.setCursor(Qt.PointingHandCursor)
        more.clicked.connect(lambda: self.opened.emit(str(path)))
        layout.addWidget(more)

    @staticmethod
    def _format_size(size: int) -> str:
        if size < 1024:
            return f"{size} B"
        if size < 1024 ** 2:
            return f"{size / 1024:.1f} KB"
        if size < 1024 ** 3:
            return f"{size / 1024 ** 2:.1f} MB"
        return f"{size / 1024 ** 3:.1f} GB"

    def _toggle_favorite(self):
        value = str(self.path)
        if self.favorites.contains(value):
            self.favorites.remove(value)
            self.star.setText("☆")
            self.favoriteChanged.emit(value, False)
        else:
            self.favorites.add(value)
            self.star.setText("★")
            self.favoriteChanged.emit(value, True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.opened.emit(str(self.path))
        super().mousePressEvent(event)


class Dashboard(QWidget):
    folderRequested = Signal(str)
    fileRequested = Signal(str)
    showAllRequested = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("dashboard")
        self.favorites = Favorites()
        self.recent = Recent()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        title = QLabel("Content")
        title.setObjectName("contentTitle")
        root.addWidget(title)

        quick_title = QLabel("Quick access")
        quick_title.setObjectName("subTitle")
        root.addWidget(quick_title)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)

        cards = [
            ("Documents", "▣", "Documents", "blue"),
            ("Photos", "●", "Images", "green"),
            ("Video", "▶", "Videos", "purple"),
            ("Presentations", "▤", "Presentations", "red"),
            ("Archives", "▥", "Archives", "violet"),
        ]
        for index, item in enumerate(cards):
            card = QuickCard(*item)
            card.opened.connect(self.folderRequested.emit)
            grid.addWidget(card, 0, index)
            grid.setColumnStretch(index, 1)

        root.addLayout(grid)

        recent_header = QHBoxLayout()
        recent_title = QLabel("Recent files")
        recent_title.setObjectName("subTitle")
        recent_header.addWidget(recent_title)
        recent_header.addStretch()
        show_all = QPushButton("Show all")
        show_all.setObjectName("showAll")
        show_all.clicked.connect(self.showAllRequested.emit)
        recent_header.addWidget(show_all)
        root.addLayout(recent_header)

        self.table = QFrame()
        self.table.setObjectName("recentTable")
        self.table_layout = QVBoxLayout(self.table)
        self.table_layout.setContentsMargins(0, 4, 0, 4)
        self.table_layout.setSpacing(4)

        header = QFrame()
        header.setObjectName("recentHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 2, 8, 2)
        name = QLabel("Name")
        date = QLabel("Date modified")
        size = QLabel("Size")
        header_layout.addWidget(name, 1)
        header_layout.addWidget(date)
        date.setFixedWidth(145)
        header_layout.addWidget(size)
        size.setFixedWidth(70)
        header_layout.addSpacing(66)
        table_layout.addWidget(header)
        root.addWidget(self.table, 1)

        self.refresh()

    def refresh(self):
        while self.table_layout.count() > 1:
            item = self.table_layout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()

        paths = []
        for raw in self.recent.load():
            path = Path(raw)
            if path.exists() and self._inside_storage(path):
                paths.append(path)

        if not paths:
            for folder in ("Documents", "Images", "Videos", "Presentations", "Archives"):
                directory = storage_path() / folder
                if directory.exists():
                    try:
                        paths.extend(sorted(directory.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)[:2])
                    except OSError:
                        pass
        paths = paths[:6]

        if not paths:
            empty = QLabel("No recent files")
            empty.setObjectName("recentEmpty")
            empty.setAlignment(Qt.AlignCenter)
            self.table_layout.addWidget(empty)
            return

        for path in paths:
            row = RecentRow(path, self.favorites)
            row.opened.connect(self._open_recent)
            self.table_layout.addWidget(row)

    def _open_recent(self, value: str):
        path = Path(value)
        if path.exists():
            self.recent.add(str(path))
            self.fileRequested.emit(str(path))

    @staticmethod
    def _inside_storage(path: Path) -> bool:
        try:
            path.resolve().relative_to(storage_path().resolve())
            return True
        except ValueError:
            return False
