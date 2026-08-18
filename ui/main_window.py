from pathlib import Path
import os

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QAction, QKeySequence, QShortcut
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QMessageBox, QMenu, QGraphicsOpacityEffect

from config import APP_NAME, APP_VERSION, WINDOW_WIDTH, WINDOW_HEIGHT, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT
from modules.clipboard import Clipboard
from modules.recent import Recent
from modules.storage_service import storage_path
from modules.ui_actions import UIActions
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
        self.selected_item = None
        self.clipboard = Clipboard()
        self.compact_view = False
        self._animations = []

        self._build_ui()
        self.ui_actions = UIActions(self)
        self._connect_signals()
        self.ui_actions.connect()
        self._setup_shortcuts()
        self._show_home(animate=False)

    def _build_ui(self):
        central = QWidget()
        central.setObjectName("appRoot")
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(16, 14, 16, 14)
        root.setSpacing(14)

        self.left_menu = LeftMenu()
        root.addWidget(self.left_menu)

        center = QWidget()
        center.setObjectName("centerPanel")
        center_layout = QVBoxLayout(center)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(9)

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
        self.explorer.contextRequested.connect(self._show_context_menu)
        self.explorer.filesDropped.connect(self._files_dropped)
        self.navigation.pathClicked.connect(self._navigate)
        self.toolbar.reload.clicked.connect(self._refresh_current)
        self.toolbar.back.clicked.connect(self._go_back)
        self.toolbar.forward.clicked.connect(self._go_forward)
        self.toolbar.search.textChanged.connect(self._search)
        self.toolbar.notification.clicked.connect(self._notifications)
        self.toolbar.view.clicked.connect(self._toggle_view)
        self.toolbar.profile.clicked.connect(self._profile)
        self.left_menu.pageChanged.connect(self._page_changed)
        self.dashboard.folderRequested.connect(self._open_storage_folder)
        self.dashboard.fileRequested.connect(self._open_recent_file)
        self.dashboard.showAllRequested.connect(lambda: self.left_menu.select("files"))
        self.right_sidebar.uploadRequested.connect(self._upload_to_current)
        self.right_sidebar.upgradeRequested.connect(self._upgrade)

    def _setup_shortcuts(self):
        shortcuts = [
            ("Ctrl+F", self._focus_search),
            ("Ctrl+N", self.ui_actions.create_folder),
            ("Ctrl+U", self.ui_actions.upload),
            ("Ctrl+C", self.ui_actions.copy),
            ("Ctrl+V", self.ui_actions.paste),
            ("F2", self.ui_actions.rename),
            ("Delete", self.ui_actions.delete),
            ("Alt+Left", self._go_back),
            ("Alt+Right", self._go_forward),
            ("F5", self._refresh_current),
        ]
        for sequence, callback in shortcuts:
            shortcut = QShortcut(QKeySequence(sequence), self)
            shortcut.activated.connect(callback)

    def _fade_in(self, widget):
        effect = QGraphicsOpacityEffect(widget)
        effect.setOpacity(0.0)
        widget.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, b"opacity", self)
        animation.setDuration(160)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        self._animations.append(animation)
        animation.finished.connect(lambda: self._drop_animation(animation, widget))
        animation.start()

    def _drop_animation(self, animation, widget):
        if widget.graphicsEffect() is not None:
            widget.setGraphicsEffect(None)
        if animation in self._animations:
            self._animations.remove(animation)
        animation.deleteLater()

    def _show_home(self, animate=True):
        self.selected_item = None
        self.dashboard.show()
        self.explorer.hide()
        self.navigation.hide()
        self.action_bar.hide()
        self.status_bar.hide()
        self.right_sidebar.refresh()
        self.left_menu.refresh_storage()
        self.dashboard.refresh()
        if animate:
            self._fade_in(self.dashboard)

    def _show_files(self, animate=True):
        self.dashboard.hide()
        self.explorer.show()
        self.navigation.show()
        self.action_bar.show()
        self.status_bar.show()
        if self.explorer.current is None:
            self.explorer.open(storage_path())
        if animate:
            self._fade_in(self.explorer)

    def _open_storage_folder(self, name):
        path = storage_path() / name
        if path.exists() and path.is_dir():
            self.left_menu.select("files")
            self.explorer.open(path)

    def _open_recent_file(self, value):
        path = Path(value)
        if not path.exists():
            self.dashboard.refresh()
            return
        Recent().add(str(path))
        if path.is_dir():
            self.left_menu.select("files")
            self.explorer.open(path)
        else:
            try:
                os.startfile(str(path))
            except OSError as exc:
                QMessageBox.warning(self, APP_NAME, str(exc))

    def _files_dropped(self, files):
        if self.dashboard.isVisible():
            self.left_menu.select("files")
        if self.explorer.current is None:
            self.explorer.open(storage_path())
        self.ui_actions.upload_files(files)

    def _refresh_current(self):
        if self.dashboard.isVisible():
            self.dashboard.refresh()
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
        self.selected_item = data
        self.status_bar.updateStatus(data["name"])

    def _show_context_menu(self, data):
        self.selected_item = data
        menu = QMenu(self)
        open_action = QAction("Open", menu)
        open_action.triggered.connect(lambda: self._open_recent_file(data["path"]))
        menu.addAction(open_action)
        menu.addSeparator()
        copy_action = QAction("Copy", menu)
        copy_action.triggered.connect(self.ui_actions.copy)
        menu.addAction(copy_action)
        rename_action = QAction("Rename", menu)
        rename_action.triggered.connect(self.ui_actions.rename)
        menu.addAction(rename_action)
        delete_action = QAction("Delete", menu)
        delete_action.triggered.connect(self.ui_actions.delete)
        menu.addAction(delete_action)
        menu.exec(self.cursor().pos())

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
        current = self.explorer.current
        if current is None:
            return
        if not text.strip():
            self.explorer.refresh()
            self.status_bar.updateStatus("Ready")
            return
        results = []
        needle = text.strip().casefold()
        try:
            for item in current.rglob("*"):
                if needle in item.name.casefold():
                    results.append(item)
        except (PermissionError, OSError):
            pass
        self.explorer.show_results(results)
        self.status_bar.updateStatus(f"Search: {len(results)}")

    def _page_changed(self, page):
        if page == "home":
            self._show_home()
            return
        if page == "settings":
            self._show_home()
            QMessageBox.information(self, APP_NAME, f"Settings\n\nStorage: local\nLimit: 5 GB\nTheme: Dark\nVersion: {APP_VERSION}")
            return
        if page == "trash":
            try:
                os.startfile("shell:RecycleBinFolder")
            except OSError:
                QMessageBox.information(self, APP_NAME, "Recycle Bin could not be opened.")
            return
        self._show_files()
        folder_map = {"documents": "Documents", "images": "Images", "videos": "Videos", "music": "Music", "archives": "Archives"}
        if page in folder_map:
            path = storage_path() / folder_map[page]
            path.mkdir(parents=True, exist_ok=True)
            self.explorer.open(path)
        elif page == "files":
            self.explorer.open(storage_path())
        elif page == "favorites":
            self._open_saved_paths(self.dashboard.favorites.load())
        elif page == "recent":
            self._open_saved_paths(self.dashboard.recent.load())

    def _open_saved_paths(self, values):
        paths = []
        for value in values:
            path = Path(value)
            if not path.exists():
                continue
            try:
                path.resolve().relative_to(storage_path().resolve())
            except ValueError:
                continue
            paths.append(path)
        self._show_files(animate=False)
        self.explorer.show_results(paths)
        self.navigation.setPath(self.explorer.current)

    def _notifications(self):
        QMessageBox.information(self, APP_NAME, "No new notifications.")

    def _profile(self):
        QMessageBox.information(self, APP_NAME, "Local profile: Ordboybro\nStorage: 5 GB")

    def _toggle_view(self):
        self.compact_view = not self.compact_view
        self.explorer.set_compact(self.compact_view)
        self.status_bar.updateStatus("Compact view" if self.compact_view else "Comfortable view")

    def _upload_to_current(self):
        if self.dashboard.isVisible():
            self.left_menu.select("files")
        if self.explorer.current is None:
            self.explorer.open(storage_path())
        self.ui_actions.upload()

    def _upgrade(self):
        QMessageBox.information(self, APP_NAME, "OrdCloud storage\n\nCurrent plan: Free\nLimit: 5 GB")
