from pathlib import Path

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout

from config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT
from modules.storage_service import storage_path
from ui.left_menu import LeftMenu
from ui.top_toolbar import TopToolbar
from ui.navigation import Navigation
from ui.action_bar import ActionBar
from ui.explorer import Explorer
from ui.status_bar import StatusBar
from ui.right_sidebar import RightSidebar
from ui.dashboard import Dashboard


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)

        self.history = []
        self.history_index = -1
        self._build_ui()
        self._connect_signals()
        self._show_home()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(20, 18, 20, 18)
        root.setSpacing(12)

        self.left_menu = LeftMenu()
        root.addWidget(self.left_menu)

        center = QWidget()
        center_layout = QVBoxLayout(center)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(10)

        self.toolbar = TopToolbar()
        self.navigation = Navigation()
        self.action_bar = ActionBar()
        self.dashboard = Dashboard()
        self.explorer = Explorer()
        self.status_bar = StatusBar()

        center_layout.addWidget(self.toolbar)
        center_layout.addWidget(self.navigation)
        center_layout.addWidget(self.action_bar)
        center_layout.addWidget(self.dashboard, 1)
        center_layout.addWidget(self.explorer, 1)
        center_layout.addWidget(self.status_bar)
        root.addWidget(center, 1)

        self.right_sidebar = RightSidebar()
        root.addWidget(self.right_sidebar)

    def _connect_signals(self):
        self.explorer.pathChanged.connect(self._path_changed)
        self.explorer.countChanged.connect(self.status_bar.updateItems)
        self.explorer.itemSelected.connect(self._item_selected)
        self.navigation.pathClicked.connect(self._navigate)
        self.toolbar.reload.clicked.connect(self._refresh_current)
        self.toolbar.back.clicked.connect(self._go_back)
        self.toolbar.forward.clicked.connect(self._go_forward)
        self.toolbar.search.textChanged.connect(self._search)
        self.left_menu.pageChanged.connect(self._page_changed)
        self.dashboard.folderRequested.connect(self._open_storage_folder)

    def _show_home(self):
        self.dashboard.show()
        self.explorer.hide()
        self.navigation.hide()
        self.action_bar.hide()
        self.status_bar.hide()
        self.right_sidebar.refresh()
        self.left_menu.refresh_storage()

    def _show_files(self):
        self.dashboard.hide()
        self.explorer.show()
        self.navigation.show()
        self.action_bar.show()
        self.status_bar.show()
        if not self.explorer.current:
            self.explorer.open(storage_path())

    def _open_storage_folder(self, name):
        path = storage_path() / name
        if path.exists() and path.is_dir():
            self.left_menu.select("files")
            self.explorer.open(path)

    def _refresh_current(self):
        if self.dashboard.isVisible():
            self.right_sidebar.refresh()
            self.left_menu.refresh_storage()
        else:
            self.explorer.refresh()
            self.right_sidebar.refresh()
            self.left_menu.refresh_storage()

    def _path_changed(self, path):
        self.navigation.setPath(path)
        if not self.history or self.history[-1] != path:
            self.history = self.history[: self.history_index + 1]
            self.history.append(path)
            self.history_index = len(self.history) - 1
        self.status_bar.updateStatus("Ready")

    def _navigate(self, path):
        self.explorer.open(path)

    def _item_selected(self, data):
        self.status_bar.updateStatus(data["name"])

    def _go_back(self):
        if self.dashboard.isVisible() or self.history_index <= 0:
            return
        self.history_index -= 1
        self.explorer.open(self.history[self.history_index])

    def _go_forward(self):
        if self.dashboard.isVisible() or self.history_index >= len(self.history) - 1:
            return
        self.history_index += 1
        self.explorer.open(self.history[self.history_index])

    def _search(self, text):
        if self.dashboard.isVisible():
            return
        if not text:
            self.explorer.refresh()
            return
        current = self.explorer.current
        results = []
        try:
            for item in current.rglob("*"):
                if text.lower() in item.name.lower():
                    results.append(item)
        except (PermissionError, OSError):
            return

        self.explorer.clear()
        from ui.file_row import FileRow
        for path in results:
            try:
                stat = path.stat()
                data = {
                    "name": path.name,
                    "icon": "▣" if path.is_dir() else "▤",
                    "size": "—" if path.is_dir() else f"{stat.st_size:,} B",
                    "modified": "",
                    "path": str(path),
                    "dir": path.is_dir(),
                }
                row = FileRow(data)
                row.opened.connect(self.explorer.open)
                row.selected.connect(self._item_selected)
                self.explorer.layout.addWidget(row)
            except (PermissionError, OSError):
                continue
        self.explorer.layout.addStretch()
        self.explorer.countChanged.emit(len(results))
        self.status_bar.updateStatus(f"Search: {len(results)}")

    def _page_changed(self, page):
        if page == "home":
            self._show_home()
            return
        self._show_files()
        folder_map = {
            "documents": "Documents",
            "images": "Images",
            "videos": "Videos",
            "music": "Music",
            "archives": "Archives",
        }
        if page in folder_map:
            path = storage_path() / folder_map[page]
            if path.exists():
                self.explorer.open(path)
        elif page == "files":
            self.explorer.open(storage_path())
