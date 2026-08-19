from pathlib import Path

from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame, QLabel
from PySide6.QtCore import Signal, Qt

from modules.file_model import FileModel
from modules.file_icons import FileIcons
from modules.storage_service import storage_path
from ui.file_row import FileRow


class Explorer(QWidget):
    pathChanged = Signal(str)
    itemSelected = Signal(dict)
    contextRequested = Signal(dict)
    countChanged = Signal(int)
    filesDropped = Signal(list)

    def __init__(self):
        super().__init__()
        self.current = storage_path()
        self._compact = False
        self._selected_row = None
        self.setAcceptDrops(True)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.body = QWidget()
        self.layout = QVBoxLayout(self.body)
        self.layout.setContentsMargins(0, 0, 4, 0)
        self.layout.setSpacing(7)
        self.scroll.setWidget(self.body)
        root.addWidget(self.scroll)

        self.open(self.current)

    def clear(self):
        self._selected_row = None
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def clear_selection(self):
        if self._selected_row is not None:
            self._selected_row.set_selected(False)
        self._selected_row = None

    def _add_rows(self, items):
        if not items:
            empty = QLabel("Эта папка пуста")
            empty.setObjectName("recentEmpty")
            empty.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(empty)
            self.layout.addStretch()
            self.countChanged.emit(0)
            return

        for data in items:
            row = FileRow(data)
            row.set_compact(self._compact)
            row.opened.connect(self.open)
            row.selected.connect(lambda value, item=row: self._select_row(item, value))
            row.contextRequested.connect(self.contextRequested.emit)
            self.layout.addWidget(row)
        self.layout.addStretch()
        self.countChanged.emit(len(items))

    def _select_row(self, row, data):
        if self._selected_row is not None and self._selected_row is not row:
            self._selected_row.set_selected(False)
        self._selected_row = row
        row.set_selected(True)
        self.itemSelected.emit(data)

    def open(self, path):
        path = Path(path)
        try:
            path.resolve().relative_to(storage_path().resolve())
        except ValueError:
            return
        if path.is_symlink() or not path.exists() or not path.is_dir():
            return

        self.current = path
        self.clear()
        items = FileModel(path).load()
        self._add_rows(items)
        self.pathChanged.emit(str(path))

    def show_results(self, paths):
        self.clear()
        items = []
        root = storage_path().resolve()
        for path in paths:
            path = Path(path)
            try:
                resolved = path.resolve()
                resolved.relative_to(root)
                if path.is_symlink():
                    continue
                stat = path.stat()
            except (ValueError, OSError):
                continue
            is_dir = path.is_dir()
            items.append({
                "name": path.name,
                "icon": FileIcons.emoji(path),
                "icon_name": FileIcons.name(path),
                "size": "—" if is_dir else self._format_size(stat.st_size),
                "bytes": 0 if is_dir else stat.st_size,
                "modified": "",
                "timestamp": stat.st_mtime,
                "path": str(path),
                "dir": is_dir,
            })
        self._add_rows(items)

    @staticmethod
    def _format_size(size):
        if size < 1024:
            return f"{size} B"
        if size < 1024 ** 2:
            return f"{size / 1024:.1f} KB"
        if size < 1024 ** 3:
            return f"{size / 1024 ** 2:.1f} MB"
        return f"{size / 1024 ** 3:.1f} GB"

    def set_compact(self, value: bool):
        self._compact = value
        self.refresh()

    def refresh(self):
        self.open(self.current)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            local_files = [url.toLocalFile() for url in event.mimeData().urls() if url.isLocalFile()]
            if local_files:
                event.acceptProposedAction()
                return
        event.ignore()

    def dropEvent(self, event):
        files = [
            url.toLocalFile()
            for url in event.mimeData().urls()
            if url.isLocalFile() and Path(url.toLocalFile()).is_file()
        ]
        if files:
            self.filesDropped.emit(files)
            event.acceptProposedAction()
        else:
            event.ignore()
