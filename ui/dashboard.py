from pathlib import Path
from datetime import datetime

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from config import ICONS_DIR
from modules.favorites import Favorites
from modules.recent import Recent
from modules.storage_service import storage_path
from ui.file_type_icon import FileTypeIcon


class QuickCard(QFrame):
    opened = Signal(str)

    def __init__(self, title: str, icon_name: str, path_name: str, color_name: str, count_unit: str = "файлов"):
        super().__init__()
        self.setObjectName("quickCard")
        self.setCursor(Qt.PointingHandCursor)
        self.path_name = path_name
        self.count_unit = count_unit
        self.setProperty("cardType", color_name)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 16)
        layout.setSpacing(9)

        icon_label = QLabel()
        icon_label.setObjectName("quickIcon")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFixedSize(64, 64)
        pixmap = QIcon(str(ICONS_DIR / icon_name)).pixmap(QSize(64, 64))
        if not pixmap.isNull():
            icon_label.setPixmap(pixmap)
        layout.addWidget(icon_label, alignment=Qt.AlignCenter)

        name = QLabel(title)
        name.setObjectName("quickTitle")
        name.setAlignment(Qt.AlignCenter)
        layout.addWidget(name)

        self.count = QLabel()
        self.count.setObjectName("quickCount")
        self.count.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.count)
        layout.addStretch(1)
        self.refresh_count()

    def refresh_count(self):
        folder = storage_path() / self.path_name
        try:
            count = sum(1 for p in folder.iterdir()) if folder.exists() else 0
        except OSError:
            count = 0
        self.count.setText(f"{count} {self.count_unit}")

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
        layout.setContentsMargins(16, 7, 14, 7)
        layout.setSpacing(14)

        icon = FileTypeIcon(path)
        layout.addWidget(icon)

        name_label = QLabel(path.name)
        name_label.setObjectName("recentName")
        layout.addWidget(name_label, 1)

        try:
            stat = path.stat()
            modified = self._relative_date(stat.st_mtime)
            size = "—" if path.is_dir() else self._format_size(stat.st_size)
        except OSError:
            modified, size = "—", "—"

        date_label = QLabel(modified)
        date_label.setObjectName("recentMeta")
        date_label.setMinimumWidth(150)
        layout.addWidget(date_label)

        size_label = QLabel(size)
        size_label.setObjectName("recentMeta")
        size_label.setMinimumWidth(80)
        layout.addWidget(size_label)

        self.star = QPushButton("★" if favorites.contains(str(path)) else "☆")
        self.star.setObjectName("recentStar")
        self.star.setFixedSize(36, 36)
        self.star.setCursor(Qt.PointingHandCursor)
        self.star.setToolTip("Убрать из избранного" if favorites.contains(str(path)) else "Добавить в избранное")
        self.star.clicked.connect(self._toggle_favorite)
        layout.addWidget(self.star)

        more = QPushButton("•••")
        more.setObjectName("recentMore")
        more.setFixedSize(36, 36)
        more.setCursor(Qt.PointingHandCursor)
        more.setToolTip("Открыть")
        more.clicked.connect(lambda: self.opened.emit(str(path)))
        layout.addWidget(more)

    @staticmethod
    def _relative_date(timestamp):
        date = datetime.fromtimestamp(timestamp)
        now = datetime.now()
        if date.date() == now.date():
            return f"Сегодня, {date:%H:%M}"
        if (now.date() - date.date()).days == 1:
            return f"Вчера, {date:%H:%M}"
        return date.strftime("%d.%m.%Y")

    @staticmethod
    def _format_size(size: int) -> str:
        if size < 1024:
            return f"{size} Б"
        if size < 1024 ** 2:
            return f"{size / 1024:.1f} КБ"
        if size < 1024 ** 3:
            return f"{size / 1024 ** 2:.1f} МБ"
        return f"{size / 1024 ** 3:.1f} ГБ"

    def _toggle_favorite(self):
        value = str(self.path)
        if self.favorites.contains(value):
            self.favorites.remove(value)
            self.star.setText("☆")
            self.star.setToolTip("Добавить в избранное")
            self.favoriteChanged.emit(value, False)
        else:
            self.favorites.add(value)
            self.star.setText("★")
            self.star.setToolTip("Убрать из избранного")
            self.favoriteChanged.emit(value, True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.opened.emit(str(self.path))
        super().mousePressEvent(event)


class Dashboard(QWidget):
    folderRequested = Signal(str)
    fileRequested = Signal(str)
    showAllRequested = Signal()
    newFolderRequested = Signal()
    uploadRequested = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("dashboard")
        self.favorites = Favorites()
        self.recent = Recent()
        self.quick_cards = []

        root = QVBoxLayout(self)
        root.setContentsMargins(30, 22, 24, 18)
        root.setSpacing(18)

        title_row = QHBoxLayout()
        title = QLabel("Быстрый доступ")
        title.setObjectName("contentTitle")
        title_row.addWidget(title)
        title_row.addStretch(1)

        new_folder = QPushButton("Новая папка")
        new_folder.setObjectName("secondaryAction")
        new_folder.setIcon(QIcon(str(ICONS_DIR / "action_new_folder.svg")))
        new_folder.setIconSize(QSize(20, 20))
        new_folder.setCursor(Qt.PointingHandCursor)
        new_folder.clicked.connect(self.newFolderRequested.emit)
        title_row.addWidget(new_folder)

        upload = QPushButton("Загрузить")
        upload.setObjectName("primaryAction")
        upload.setIcon(QIcon(str(ICONS_DIR / "ui_upload.svg")))
        upload.setIconSize(QSize(20, 20))
        upload.setCursor(Qt.PointingHandCursor)
        upload.clicked.connect(self.uploadRequested.emit)
        title_row.addWidget(upload)
        root.addLayout(title_row)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(12)
        cards = [
            ("Документы", "documents.svg", "Documents", "blue"),
            ("Фото", "images.svg", "Images", "green"),
            ("Видео", "videos.svg", "Videos", "purple"),
            ("Презентации", "presentations.svg", "Presentations", "red"),
            ("Архивы", "archives.svg", "Archives", "violet"),
        ]
        for index, item in enumerate(cards):
            card = QuickCard(*item)
            card.opened.connect(self.folderRequested.emit)
            self.quick_cards.append(card)
            grid.addWidget(card, 0, index)
            grid.setColumnStretch(index, 1)
        root.addLayout(grid)

        recent_header = QHBoxLayout()
        recent_title = QLabel("Недавние файлы")
        recent_title.setObjectName("subTitle")
        recent_header.addWidget(recent_title)
        recent_header.addStretch(1)
        show_all = QPushButton("Показать все")
        show_all.setObjectName("showAll")
        show_all.setCursor(Qt.PointingHandCursor)
        show_all.clicked.connect(self.showAllRequested.emit)
        recent_header.addWidget(show_all)
        root.addLayout(recent_header)

        self.table = QFrame()
        self.table.setObjectName("recentTable")
        self.table_layout = QVBoxLayout(self.table)
        self.table_layout.setContentsMargins(0, 0, 0, 0)
        self.table_layout.setSpacing(0)

        header = QFrame()
        header.setObjectName("recentHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(18, 0, 14, 0)
        header_layout.setSpacing(14)
        header_layout.addSpacing(42)
        name = QLabel("Название  ↑")
        date = QLabel("Дата изменения")
        size = QLabel("Размер")
        header_layout.addWidget(name, 1)
        date.setMinimumWidth(150)
        header_layout.addWidget(date)
        size.setMinimumWidth(80)
        header_layout.addWidget(size)
        header_layout.addSpacing(72)
        self.table_layout.addWidget(header)
        root.addWidget(self.table, 1)
        self.refresh()

    def refresh(self):
        for card in self.quick_cards:
            card.refresh_count()

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

        unique = []
        seen = set()
        for path in paths:
            key = str(path.resolve()).casefold()
            if key not in seen:
                seen.add(key)
                unique.append(path)
        paths = unique[:6]

        if not paths:
            empty = QLabel("Здесь появятся недавно открытые файлы")
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
