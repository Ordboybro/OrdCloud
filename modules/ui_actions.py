from pathlib import Path
import shutil

from PySide6.QtWidgets import QFileDialog, QInputDialog, QMessageBox

from modules.storage_service import storage, storage_path


class UIActions:

    def __init__(self, window):
        self.window = window

    @property
    def explorer(self):
        return self.window.explorer

    @property
    def selected(self):
        return getattr(self.window, "selected_item", None)

    def connect(self):
        bar = self.window.action_bar
        bar.new_folder.clicked.connect(self.create_folder)
        bar.upload.clicked.connect(self.upload)
        bar.copy.clicked.connect(self.copy)
        bar.paste.clicked.connect(self.paste)
        bar.rename.clicked.connect(self.rename)
        bar.delete.clicked.connect(self.delete)

        self.window.left_menu.pageChanged.connect(self.page_changed)

    def _selected_path(self):
        if not self.selected:
            QMessageBox.information(
                self.window,
                "OrdCloud",
                "Select a file or folder first.",
            )
            return None

        path = Path(self.selected["path"])
        if not path.exists():
            self.explorer.refresh()
            return None

        try:
            path.resolve().relative_to(storage_path().resolve())
        except ValueError:
            QMessageBox.warning(
                self.window,
                "OrdCloud",
                "The selected path is outside storage.",
            )
            return None

        return path

    @staticmethod
    def _relative(path):
        return str(
            Path(path).resolve().relative_to(
                storage_path().resolve()
            )
        )

    def create_folder(self):
        name, ok = QInputDialog.getText(
            self.window,
            "New Folder",
            "Folder name:",
        )
        if not ok:
            return

        name = name.strip()
        if not name or Path(name).name != name or name in {".", ".."}:
            QMessageBox.warning(self.window, "OrdCloud", "Invalid folder name.")
            return

        try:
            storage.create_folder(
                self._relative(self.explorer.current),
                name,
            )
            self.explorer.refresh()
        except FileExistsError:
            QMessageBox.warning(
                self.window,
                "OrdCloud",
                "A folder with this name already exists.",
            )
        except (OSError, ValueError) as exc:
            QMessageBox.critical(self.window, "OrdCloud", str(exc))

    def upload(self):
        files, _ = QFileDialog.getOpenFileNames(
            self.window,
            "Upload files",
            str(Path.home()),
            "All files (*.*)",
        )
        if not files:
            return

        try:
            for source in files:
                source = Path(source)
                destination = self.explorer.current / source.name

                if destination.exists():
                    answer = QMessageBox.question(
                        self.window,
                        "OrdCloud",
                        f"{source.name} already exists. Replace it?",
                        QMessageBox.Yes | QMessageBox.No,
                    )
                    if answer != QMessageBox.Yes:
                        continue
                    if destination.is_dir():
                        shutil.rmtree(destination)
                    else:
                        destination.unlink()

                if not storage.can_add(source.stat().st_size):
                    raise OSError("Storage limit exceeded.")

                shutil.copy2(source, destination)

            self.explorer.refresh()
        except (OSError, PermissionError) as exc:
            QMessageBox.critical(self.window, "Upload failed", str(exc))

    def copy(self):
        path = self._selected_path()
        if not path:
            return

        self.window.clipboard.copy(path)
        self.window.status_bar.updateStatus("Copied")

    def paste(self):
        clipboard = self.window.clipboard
        if not clipboard.has_data() or clipboard.path is None:
            QMessageBox.information(self.window, "OrdCloud", "Clipboard is empty.")
            return

        source = clipboard.path
        if not source.exists():
            clipboard.clear()
            return

        destination = self.explorer.current / source.name
        if destination.exists():
            QMessageBox.warning(
                self.window,
                "OrdCloud",
                "An item with this name already exists here.",
            )
            return

        try:
            if clipboard.mode == "copy":
                if source.is_dir():
                    shutil.copytree(source, destination)
                else:
                    if not storage.can_add(source.stat().st_size):
                        raise OSError("Storage limit exceeded.")
                    shutil.copy2(source, destination)
            else:
                shutil.move(str(source), str(destination))

            clipboard.clear()
            self.explorer.refresh()
        except (OSError, PermissionError) as exc:
            QMessageBox.critical(self.window, "Paste failed", str(exc))

    def rename(self):
        path = self._selected_path()
        if not path:
            return

        name, ok = QInputDialog.getText(
            self.window,
            "Rename",
            "New name:",
            text=path.name,
        )
        if not ok:
            return

        name = name.strip()
        if not name or Path(name).name != name or name in {".", ".."}:
            QMessageBox.warning(self.window, "OrdCloud", "Invalid name.")
            return

        try:
            storage.rename(self._relative(path), name)
            self.explorer.refresh()
        except (OSError, ValueError) as exc:
            QMessageBox.critical(self.window, "Rename failed", str(exc))

    def delete(self):
        path = self._selected_path()
        if not path:
            return

        answer = QMessageBox.question(
            self.window,
            "Delete",
            f"Move '{path.name}' to the Recycle Bin?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return

        try:
            from send2trash import send2trash
            send2trash(str(path))
            self.window.selected_item = None
            self.explorer.refresh()
        except OSError as exc:
            QMessageBox.critical(self.window, "Delete failed", str(exc))

    def page_changed(self, page):
        if page in {"home", "files", "cloud", "uploads"}:
            self.explorer.open(storage_path())
