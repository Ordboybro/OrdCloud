from pathlib import Path

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

from modules.storage_service import storage_path


class QuickCard(QFrame):
    opened = Signal(str)

    def __init__(self, title, icon, path_name):
        super().__init__()
        self.setObjectName("quickCard")
        self.setCursor(Qt.PointingHandCursor)
        self.path_name = path_name

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(10)

        icon_label = QLabel(icon)
        icon_label.setObjectName("quickIcon")
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

    def _count(self):
        folder = storage_path() / self.path_name
        try:
            if folder.exists():
                return f"{sum(1 for p in folder.iterdir())} files"
        except OSError:
            pass
        return "0 files"

    def mousePressEvent(self, event):
        self.opened.emit(self.path_name)
        super().mousePressEvent(event)


class RecentRow(QFrame):
    def __init__(self, name, modified, size, icon):
        super().__init__()
        self.setObjectName("recentRow")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 4, 8, 4)
        layout.setSpacing(10)

        icon_label = QLabel(icon)
        icon_label.setObjectName("recentIcon")
        icon_label.setFixedWidth(28)
        layout.addWidget(icon_label)

        name_label = QLabel(name)
        name_label.setObjectName("recentName")
        layout.addWidget(name_label, 1)

        date_label = QLabel(modified)
        date_label.setObjectName("recentMeta")
        date_label.setFixedWidth(150)
        layout.addWidget(date_label)

        size_label = QLabel(size)
        size_label.setObjectName("recentMeta")
        size_label.setFixedWidth(70)
        layout.addWidget(size_label)

        star = QPushButton("☆")
        star.setObjectName("recentStar")
        star.setFixedSize(28, 28)
        star.setCursor(Qt.PointingHandCursor)
        layout.addWidget(star)

        more = QPushButton("•••")
        more.setObjectName("recentMore")
        more.setFixedSize(30, 28)
        more.setCursor(Qt.PointingHandCursor)
        layout.addWidget(more)


class Dashboard(QWidget):
    folderRequested = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("dashboard")

        root = QVBoxLayout(self)
        root.setContentsMargins(8, 2, 8, 0)
        root.setSpacing(14)

        title = QLabel("Content")
        title.setObjectName("contentTitle")
        root.addWidget(title)

        quick_title_row = QHBoxLayout()
        quick_title = QLabel("Quick access")
        quick_title.setObjectName("subTitle")
        quick_title_row.addWidget(quick_title)
        quick_title_row.addStretch()
        root.addLayout(quick_title_row)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)

        cards = [
            ("Documents", "▣", "Documents"),
            ("Photos", "◉", "Images"),
            ("Video", "▶", "Videos"),
            ("Presentations", "▤", "Documents"),
            ("Archives", "▥", "Archives"),
        ]
        for index, (title_text, icon, folder) in enumerate(cards):
            card = QuickCard(title_text, icon, folder)
            card.opened.connect(self.folderRequested.emit)
            grid.addWidget(card, 0, index)

        root.addLayout(grid)

        recent_header = QHBoxLayout()
        recent_title = QLabel("Recent files")
        recent_title.setObjectName("subTitle")
        recent_header.addWidget(recent_title)
        recent_header.addStretch()
        show_all = QPushButton("Show all")
        show_all.setObjectName("showAll")
        recent_header.addWidget(show_all)
        root.addLayout(recent_header)

        table = QFrame()
        table.setObjectName("recentTable")
        table_layout = QVBoxLayout(table)
        table_layout.setContentsMargins(0, 4, 0, 4)
        table_layout.setSpacing(4)

        header = QFrame()
        header.setObjectName("recentHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 2, 8, 2)
        header_layout.addWidget(QLabel("Name"), 1)
        header_layout.addWidget(QLabel("Date modified"), 0)
        header_layout.itemAt(1).widget().setFixedWidth(150)
        header_layout.addWidget(QLabel("Size"), 0)
        header_layout.itemAt(2).widget().setFixedWidth(70)
        header_layout.addSpacing(66)
        table_layout.addWidget(header)

        samples = [
            ("Study", "Today, 14:32", "—", "▣"),
            ("Nature.jpg", "Today, 12:18", "2.3 MB", "◉"),
            ("Report.pdf", "Yesterday, 21:07", "1.5 MB", "▤"),
            ("Report.docx", "Yesterday, 18:20", "1.1 MB", "▤"),
            ("Table.xlsx", "28 May 2025", "312 KB", "▤"),
            ("Archive.zip", "27 May 2025", "5.6 MB", "▥"),
        ]
        for row in samples:
            table_layout.addWidget(RecentRow(*row))

        root.addWidget(table, 1)
