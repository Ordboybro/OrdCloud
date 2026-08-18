from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
)

from config import (
    APP_NAME,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    MIN_WINDOW_HEIGHT,
)

from ui.left_menu import LeftMenu
from ui.top_toolbar import TopToolbar
from ui.navigation import Navigation
from ui.action_bar import ActionBar
from ui.explorer import Explorer
from ui.status_bar import StatusBar
from ui.right_sidebar import RightSidebar


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)

        self.resize(
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
        )

        self.setMinimumSize(
            MIN_WINDOW_WIDTH,
            MIN_WINDOW_HEIGHT,
        )

        self.history = []
        self.history_index = -1

        self._build_ui()
        self._connect_signals()

    def _build_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)

        root.setContentsMargins(
            12,
            12,
            12,
            12,
        )

        root.setSpacing(12)

        self.left_menu = LeftMenu()

        root.addWidget(
            self.left_menu
        )

        center = QWidget()

        center_layout = QVBoxLayout(center)

        center_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        center_layout.setSpacing(10)

        self.toolbar = TopToolbar()
        self.navigation = Navigation()
        self.action_bar = ActionBar()
        self.explorer = Explorer()
        self.status_bar = StatusBar()

        center_layout.addWidget(
            self.toolbar
        )

        center_layout.addWidget(
            self.navigation
        )

        center_layout.addWidget(
            self.action_bar
        )

        center_layout.addWidget(
            self.explorer,
            1,
        )

        center_layout.addWidget(
            self.status_bar
        )

        root.addWidget(
            center,
            1,
        )

        self.right_sidebar = RightSidebar()

        root.addWidget(
            self.right_sidebar
        )

    def _connect_signals(self):

        self.explorer.pathChanged.connect(
            self._path_changed
        )

        self.explorer.countChanged.connect(
            self.status_bar.updateItems
        )

        self.explorer.itemSelected.connect(
            self._item_selected
        )

        self.navigation.pathClicked.connect(
            self._navigate
        )

        self.toolbar.reload.clicked.connect(
            self.explorer.refresh
        )

        self.toolbar.back.clicked.connect(
            self._go_back
        )

        self.toolbar.forward.clicked.connect(
            self._go_forward
        )

        self.toolbar.search.textChanged.connect(
            self._search
        )

        self.left_menu.pageChanged.connect(
            self._page_changed
        )

    def _path_changed(self, path):

        self.navigation.setPath(path)

        if not self.history or self.history[-1] != path:

            self.history.append(path)
            self.history_index = len(
                self.history
            ) - 1

        self.status_bar.updateStatus(
            "Готово"
        )

    def _navigate(self, path):

        self.explorer.open(path)

    def _item_selected(self, data):

        self.status_bar.updateStatus(
            data["name"]
        )

    def _go_back(self):

        if self.history_index <= 0:
            return

        self.history_index -= 1

        path = self.history[
            self.history_index
        ]

        self.explorer.open(path)

    def _go_forward(self):

        if (
            self.history_index
            >= len(self.history) - 1
        ):
            return

        self.history_index += 1

        path = self.history[
            self.history_index
        ]

        self.explorer.open(path)

    def _search(self, text):

        if not text:

            self.explorer.refresh()
            return

        current = self.explorer.current

        results = []

        try:

            for item in current.rglob("*"):

                if text.lower() in item.name.lower():
                    results.append(item)

        except (
            PermissionError,
            OSError,
        ):
            return

        self.explorer.clear()

        from ui.file_row import FileRow

        for path in results:

            try:

                stat = path.stat()

                data = {
                    "name": path.name,
                    "icon": (
                        "📁"
                        if path.is_dir()
                        else "📄"
                    ),
                    "size": (
                        "—"
                        if path.is_dir()
                        else f"{stat.st_size:,} B"
                    ),
                    "modified": "",
                    "path": str(path),
                    "dir": path.is_dir(),
                }

                row = FileRow(data)

                row.opened.connect(
                    self.explorer.open
                )

                row.selected.connect(
                    self._item_selected
                )

                self.explorer.layout.addWidget(
                    row
                )

            except (
                PermissionError,
                OSError,
            ):
                continue

        self.explorer.layout.addStretch()

        self.explorer.countChanged.emit(
            len(results)
        )

        self.status_bar.updateStatus(
            f"Поиск: {len(results)}"
        )

    def _page_changed(self, page):

        if page in (
            "home",
            "files",
        ):

            self.explorer.open(
                Path.home()
            )

        elif page == "favorites":

            self.status_bar.updateStatus(
                "Избранное"
            )

        elif page == "recent":

            self.status_bar.updateStatus(
                "Недавние файлы"
            )

        elif page == "cloud":

            self.status_bar.updateStatus(
                "Облачное хранилище"
            )

        elif page == "uploads":

            self.status_bar.updateStatus(
                "Загрузки"
            )

        elif page == "trash":

            self.status_bar.updateStatus(
                "Корзина"
            )

        elif page == "settings":

            self.status_bar.updateStatus(
                "Настройки"
            )
