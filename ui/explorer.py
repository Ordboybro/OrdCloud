from pathlib import Path

from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame
from PySide6.QtCore import Signal, Qt

from modules.file_model import FileModel
from modules.storage_service import storage_path
from ui.file_row import FileRow


class Explorer(QWidget):
    pathChanged = Signal(str)
    itemSelected = Signal(dict)
    countChanged = Signal(int)

    def __init__(self):
        super().__init__()
        self.current = storage_path()
        self._compact = False

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
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _add_rows(self, items):
        for data in items:
            row = FileRow(data)
            row.set_compact(self._compact)
            row.opened.connect(self.open)
            row.selected.connect(self.itemSelected.emit)
            self.layout.addWidget(row)
        self.layout.addStretch()
        self.countChanged.emit(len(items))

    def open(self, path):
        path = Path(path)
        try:
            path.resolve().relative_to(storage_path().resolve())
        except ValueError:
            return
        if not path.exists() or not path.is_dir():
            return

        self.current = path
        self.clear()
        model = FileModel(path)
        items = model.load()
        self._add_rows(items)
        self.pathChanged.emit(str(path))

    def show_results(self, paths):
        self.clear()
        items = []
        for path in paths:
            path = Path(path)
            try:
                stat = path.stat()
            except OSError:
                continue
            items.append({
                "name": path.name,
                "icon": "▣" if path.is_dir() else "▤",
                "size": "—" if path.is_dir() else self._format_size(stat.st_size),
                "modified": stat.st_mtime,
                "path": str(path),
                "dir": path.is_dir(),
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
