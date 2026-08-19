from pathlib import Path
import shutil

from PySide6.QtWidgets import QFileDialog, QInputDialog, QMessageBox

from modules.recent import Recent
from modules.storage_service import storage, storage_path


class UIActions:
    """Commands triggered by the toolbar and keyboard shortcuts."""

    def __init__(self, window):
        self.window = window
        self.recent = Recent()

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

    def _current_path(self):
        current = self.explorer.current
        if current is None:
            current = storage_path()
            self.explorer.open(current)

        current = Path(current).resolve()
        try:
            current.relative_to(storage_path().resolve())
        except ValueError:
            QMessageBox.warning(self.window, "OrdCloud", "Текущая папка находится вне хранилища.")
            return None
        if not current.is_dir():
            QMessageBox.warning(self.window, "OrdCloud", "Текущее расположение не является папкой.")
            return None
        return current

    def _selected_path(self):
        if not self.selected:
            QMessageBox.information(self.window, "OrdCloud", "Сначала выбери файл или папку.")
            return None

        path = Path(self.selected["path"]).resolve()
        if not path.exists():
            self.window.selected_item = None
            self.explorer.refresh()
            return None

        try:
            path.relative_to(storage_path().resolve())
        except ValueError:
            QMessageBox.warning(self.window, "OrdCloud", "Выбранный путь находится вне хранилища.")
            return None
        return path

    @staticmethod
    def _relative(path):
        return str(Path(path).resolve().relative_to(storage_path().resolve()))

    @staticmethod
    def _valid_name(name: str) -> bool:
        name = name.strip()
        if not name or Path(name).name != name or name in {".", ".."}:
            return False
        return not any(char in name for char in '<>:"/\\|?*')

    def _refresh(self):
        if not self.window.dashboard.isVisible():
            self.explorer.refresh()
        self.window.dashboard.refresh()
        self.window.right_sidebar.refresh()
        self.window.left_menu.refresh_storage()

    def create_folder(self):
        current = self._current_path()
        if current is None:
            return
        name, ok = QInputDialog.getText(self.window, "Новая папка", "Название папки:")
        if not ok:
            return
        name = name.strip()
        if not self._valid_name(name):
            QMessageBox.warning(self.window, "OrdCloud", "Некорректное имя папки.")
            return
        try:
            storage.create_folder(self._relative(current), name)
            self._refresh()
        except FileExistsError:
            QMessageBox.warning(self.window, "OrdCloud", "Папка с таким именем уже существует.")
        except (OSError, ValueError) as exc:
            QMessageBox.critical(self.window, "OrdCloud", str(exc))

    def upload(self):
        files, _ = QFileDialog.getOpenFileNames(
            self.window,
            "Загрузить файлы",
            str(Path.home()),
            "Все файлы (*.*)",
        )
        if files:
            self.upload_files(files)

    def upload_files(self, files):
        current = self._current_path()
        if current is None:
            return

        for source_name in files:
            source = Path(source_name)
            try:
                if not source.exists() or not source.is_file():
                    continue

                destination = current / source.name
                old_size = destination.stat().st_size if destination.is_file() else 0

                if destination.exists():
                    answer = QMessageBox.question(
                        self.window,
                        "OrdCloud",
                        f"{source.name} уже существует. Заменить его?",
                        QMessageBox.Yes | QMessageBox.No,
                    )
                    if answer != QMessageBox.Yes:
                        continue
                    if destination.is_dir():
                        shutil.rmtree(destination)
                    else:
                        destination.unlink()

                size = source.stat().st_size
                if not storage.can_add(max(0, size - old_size)):
                    raise OSError("Превышен лимит хранилища 5 ГБ.")

                shutil.copy2(source, destination)
                self.recent.add(str(destination))
            except (OSError, PermissionError) as exc:
                QMessageBox.critical(self.window, "Ошибка загрузки", f"{source.name}: {exc}")

        self._refresh()

    def copy(self):
        path = self._selected_path()
        if not path:
            return
        self.window.clipboard.copy(path)
        self.window.status_bar.updateStatus("Скопировано")

    def paste(self):
        current = self._current_path()
        if current is None:
            return

        clipboard = self.window.clipboard
        if not clipboard.has_data() or clipboard.path is None:
            QMessageBox.information(self.window, "OrdCloud", "Буфер обмена пуст.")
            return

        source = Path(clipboard.path).resolve()
        if not source.exists():
            clipboard.clear()
            return

        try:
            source.relative_to(storage_path().resolve())
        except ValueError:
            QMessageBox.warning(self.window, "OrdCloud", "Элемент буфера находится вне хранилища.")
            clipboard.clear()
            return

        destination = (current / source.name).resolve()
        if source == destination:
            return
        if source.is_dir():
            try:
                current.relative_to(source)
            except ValueError:
                pass
            else:
                QMessageBox.warning(self.window, "OrdCloud", "Нельзя переместить папку внутрь самой себя.")
                return

        if destination.exists():
            QMessageBox.warning(self.window, "OrdCloud", "Элемент с таким именем уже существует здесь.")
            return

        try:
            if clipboard.mode == "copy":
                if source.is_dir():
                    size = sum(p.stat().st_size for p in source.rglob("*") if p.is_file())
                    if not storage.can_add(size):
                        raise OSError("Превышен лимит хранилища 5 ГБ.")
                    shutil.copytree(source, destination)
                else:
                    if not storage.can_add(source.stat().st_size):
                        raise OSError("Превышен лимит хранилища 5 ГБ.")
                    shutil.copy2(source, destination)
            else:
                shutil.move(str(source), str(destination))

            self.recent.add(str(destination))
            clipboard.clear()
            self._refresh()
        except (OSError, PermissionError) as exc:
            QMessageBox.critical(self.window, "Ошибка вставки", str(exc))

    def rename(self):
        path = self._selected_path()
        if not path:
            return
        name, ok = QInputDialog.getText(self.window, "Переименовать", "Новое имя:", text=path.name)
        if not ok:
            return
        name = name.strip()
        if not self._valid_name(name):
            QMessageBox.warning(self.window, "OrdCloud", "Некорректное имя.")
            return
        try:
            new_path = storage.rename(self._relative(path), name)
            self.recent.add(str(new_path))
            self.window.selected_item = None
            self._refresh()
        except (OSError, ValueError) as exc:
            QMessageBox.critical(self.window, "Ошибка переименования", str(exc))

    def delete(self):
        path = self._selected_path()
        if not path:
            return

        answer = QMessageBox.question(
            self.window,
            "Удалить",
            f"Переместить «{path.name}» в корзину?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return

        try:
            from send2trash import send2trash
            send2trash(str(path))
            self.window.selected_item = None
            self._refresh()
        except OSError as exc:
            QMessageBox.critical(self.window, "Ошибка удаления", str(exc))
