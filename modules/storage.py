from pathlib import Path
import shutil
import time


class StorageManager:
    """Safe local storage operations constrained to a single root directory."""

    _SNAPSHOT_TTL = 0.75

    def __init__(self, root: Path, max_bytes: int):
        self.root = Path(root).resolve()
        self.max_bytes = max(0, int(max_bytes))
        self.root.mkdir(parents=True, exist_ok=True)
        self._snapshot = None
        self._snapshot_at = 0.0

    def resolve(self, relative_path=""):
        """Resolve a path while keeping it strictly inside storage.

        Relative paths are preferred, but absolute paths are accepted when
        they already point inside the storage root. The root itself remains
        a protected location and is never returned for an item operation.
        """
        candidate = Path(relative_path)
        target = candidate.resolve() if candidate.is_absolute() else (self.root / candidate).resolve()
        try:
            target.relative_to(self.root)
        except ValueError as exc:
            raise ValueError("Path escapes storage") from exc
        if target == self.root:
            raise ValueError("Storage root is not an item path")
        return target

    def _raw_path(self, relative_path="") -> Path:
        """Build an absolute path without following the final symlink."""
        relative = Path(relative_path)
        return relative if relative.is_absolute() else self.root / relative

    @staticmethod
    def _reject_symlink(path: Path) -> None:
        if path.is_symlink():
            raise ValueError("Symbolic links are not supported")

    def invalidate_stats(self):
        self._snapshot = None
        self._snapshot_at = 0.0

    def get_snapshot(self, force=False):
        """Return one short-lived filesystem scan shared by all statistics."""
        now = time.monotonic()
        if not force and self._snapshot is not None and now - self._snapshot_at < self._SNAPSHOT_TTL:
            return {**self._snapshot, "categories": self._snapshot["categories"].copy()}

        total = 0
        files = 0
        directories = 0
        categories = {"Документы": 0, "Изображения": 0, "Видео": 0, "Другое": 0}
        document_exts = {".txt", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".csv", ".py", ".json", ".md"}
        image_exts = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg"}
        video_exts = {".mp4", ".mkv", ".avi", ".mov", ".webm"}

        try:
            for path in self.root.rglob("*"):
                try:
                    if path.is_symlink():
                        continue
                    if path.is_dir():
                        directories += 1
                        continue
                    if not path.is_file():
                        continue
                    size = path.stat().st_size
                    total += size
                    files += 1
                    suffix = path.suffix.lower()
                    if suffix in document_exts:
                        categories["Документы"] += size
                    elif suffix in image_exts:
                        categories["Изображения"] += size
                    elif suffix in video_exts:
                        categories["Видео"] += size
                    else:
                        categories["Другое"] += size
                except OSError:
                    continue
        except OSError:
            pass

        self._snapshot = {
            "size": total,
            "files": files,
            "directories": directories,
            "categories": categories.copy(),
        }
        self._snapshot_at = now
        return {**self._snapshot, "categories": categories.copy()}

    def get_size(self) -> int:
        return self.get_snapshot()["size"]

    def get_free(self) -> int:
        return max(0, self.max_bytes - self.get_size())

    def get_usage_percent(self) -> float:
        if self.max_bytes <= 0:
            return 0.0
        return min(100.0, self.get_size() / self.max_bytes * 100.0)

    def can_add(self, size: int) -> bool:
        size = int(size)
        return size >= 0 and self.get_size() + size <= self.max_bytes

    def create_folder(self, parent="", name="New Folder"):
        name = name.strip()
        if not name or Path(name).name != name or name in {".", ".."}:
            raise ValueError("Invalid folder name")
        parent_path = self.resolve(parent) if parent else self.root
        self._reject_symlink(parent_path)
        if not parent_path.is_dir():
            raise NotADirectoryError(parent_path)
        target = parent_path / name
        if target.exists() or target.is_symlink():
            raise FileExistsError(target)
        target.mkdir(parents=False, exist_ok=False)
        self.invalidate_stats()
        return target.resolve()

    def delete(self, relative_path):
        raw = self._raw_path(relative_path)
        if raw.resolve() == self.root:
            raise ValueError("Cannot delete storage root")
        self._reject_symlink(raw)
        target = self.resolve(relative_path)
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()
        else:
            raise FileNotFoundError(target)
        self.invalidate_stats()

    def rename(self, relative_path, new_name):
        new_name = new_name.strip()
        if not new_name or Path(new_name).name != new_name or new_name in {".", ".."}:
            raise ValueError("Invalid name")
        raw = self._raw_path(relative_path)
        self._reject_symlink(raw)
        target = self.resolve(relative_path)
        new_path = target.parent / new_name
        if new_path.exists() or new_path.is_symlink():
            raise FileExistsError("Target already exists")
        new_path = new_path.resolve()
        try:
            new_path.relative_to(self.root)
        except ValueError as exc:
            raise ValueError("Path escapes storage") from exc
        target.rename(new_path)
        self.invalidate_stats()
        return new_path

    def copy_file(self, source, destination):
        source = Path(source)
        if source.is_symlink():
            raise ValueError("Symbolic links are not supported")
        source = source.resolve()
        if not source.is_file():
            raise FileNotFoundError(source)
        destination = self.resolve(destination)
        self._reject_symlink(destination)
        if destination == source:
            raise ValueError("Source and destination are identical")
        if destination.exists():
            raise FileExistsError(destination)
        if not self.can_add(source.stat().st_size):
            raise OSError("Storage limit exceeded")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        self.invalidate_stats()
        return destination

    def move_file(self, source, destination):
        source = Path(source)
        if source.is_symlink():
            raise ValueError("Symbolic links are not supported")
        source = source.resolve()
        if not source.is_file():
            raise FileNotFoundError(source)
        destination = self.resolve(destination)
        self._reject_symlink(destination)
        if destination == source:
            raise ValueError("Source and destination are identical")
        if destination.exists():
            raise FileExistsError(destination)
        try:
            source.relative_to(self.root)
            source_inside_storage = True
        except ValueError:
            source_inside_storage = False
        if not source_inside_storage and not self.can_add(source.stat().st_size):
            raise OSError("Storage limit exceeded")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
        self.invalidate_stats()
        return destination

    def exists(self, relative_path):
        try:
            return self.resolve(relative_path).exists()
        except ValueError:
            return False

    def is_file(self, relative_path):
        try:
            return self.resolve(relative_path).is_file()
        except ValueError:
            return False

    def is_dir(self, relative_path):
        try:
            return self.resolve(relative_path).is_dir()
        except ValueError:
            return False
