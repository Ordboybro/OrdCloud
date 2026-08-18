from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QFrame,
)

from PySide6.QtCore import (
    Signal,
    Qt,
)

from modules.file_model import FileModel
from modules.storage_service import (
    storage_path,
)

from ui.file_row import FileRow


class Explorer(QWidget):

    pathChanged = Signal(str)
    itemSelected = Signal(dict)
    countChanged = Signal(int)

    def __init__(self):
        super().__init__()

        self.current = storage_path()

        root = QVBoxLayout(self)

        root.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        root.setSpacing(0)

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setFrameShape(
            QFrame.NoFrame
        )

        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.body = QWidget()

        self.layout = QVBoxLayout(
            self.body
        )

        self.layout.setContentsMargins(
            0,
            0,
            4,
            0,
        )

        self.layout.setSpacing(7)

        self.scroll.setWidget(
            self.body
        )

        root.addWidget(
            self.scroll
        )

        self.open(
            self.current
        )

    def clear(self):

        while self.layout.count():

            item = self.layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

    def open(self, path):

        path = Path(path)

        try:

            path.resolve().relative_to(
                storage_path().resolve()
            )

        except ValueError:

            return

        if not path.exists():
            return

        if not path.is_dir():
            return

        self.current = path

        self.clear()

        model = FileModel(path)

        items = model.load()

        for data in items:

            row = FileRow(data)

            row.opened.connect(
                self.open
            )

            row.selected.connect(
                self.itemSelected.emit
            )

            self.layout.addWidget(
                row
            )

        self.layout.addStretch()

        self.countChanged.emit(
            len(items)
        )

        self.pathChanged.emit(
            str(path)
        )

    def refresh(self):

        self.open(
            self.current
        )
