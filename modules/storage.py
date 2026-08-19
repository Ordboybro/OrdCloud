from pathlib import Path
import shutil


class StorageManager:
    """Safe local storage operations constrained to a single root directory."""

    def __init__(self, root: Path, max_bytes: int):
        self.root = Path(root).resolve()
        self.max_bytes = max(0, int(max_bytes))
        self.root.mkdir(parents=True, exist_ok=True)

    def resolve(self, relative_path=""):
        relative = Path(relative_path)
        if relative.is_absolute():
            raise ValueError("Absolute paths are not allowed")

        target = (self.root / relative).resolve()
        try:
            target.relative_to(self.root)
        except ValueError as exc:
            raise ValueError("Path escapes storage") from exc
        return target

    def get_size(self) -> int:
        total = 0
        try:
            iterator = self.root.rglob("*")
            for path in iterator:
                try:
                    if path.is_file():
                        total += path.stat().st_size
                except OSError:
                    continue
        except OSError:
            return total
        return total

    def get_free(self) -> int:
        return max(0, self.max_bytes - self.get_size())

    def get_usage_percent(self) -> float:
        if self.max_bytes <= 0:
            return 0.0
        return min(100.0, self.get_size() / self.max_bytes * 100.0)

    def can_add(self, size: int) -> bool:
        size = int(size)
        if size < 0:
            return False
        return self.get_size() + size <= self.max_bytes

    def create_folder(self, parent="", name="New Folder"):
        name = name.strip()
        if not name:
            raise ValueError("Folder name cannot be empty")
        if Path(name).name != name or name in {".", ".."}:
            raise ValueError("Invalid folder name")

        parent_path = self.resolve(parent)
        if not parent_path.is_dir():
            raise NotADirectoryError(parent_path)

        target = (parent_path / name).resolve()
        try:
            target.relative_to(self.root)
        except ValueError as exc:
            raise ValueError("Path escapes storage") from exc

        target.mkdir(parents=False, exist_ok=False)
        return target

    def delete(self, relative_path):
        target = self.resolve(relative_path)
        if target == self.root:
            raise ValueError("Cannot delete storage root")
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()

    def rename(self, relative_path, new_name):
        new_name = new_name.strip()
        if not new_name:
            raise ValueError("New name cannot be empty")
        if Path(new_name).name != new_name or new_name in {".", ".."}:
            raise ValueError("Invalid name")

        target = self.resolve(relative_path)
        if target == self.root:
            raise ValueError("Cannot rename storage root")
        if not target.exists():
            raise FileNotFoundError(target)

        new_path = (target.parent / new_name).resolve()
        try:
            new_path.relative_to(self.root)
        except ValueError as exc:
            raise ValueError("Path escapes storage") from exc
        if new_path.exists():
            raise FileExistsError("Target already exists")

        target.rename(new_path)
        return new_path

    def copy_file(self, source, destination):
        source = Path(source).resolve()
        if not source.is_file():
            raise FileNotFoundError(source)
        destination = self.resolve(destination)
        if destination == source:
            raise ValueError("Source and destination are identical")
        if destination.exists():
            raise FileExistsError(destination)
        if not self.can_add(source.stat().st_size):
            raise OSError("Storage limit exceeded")

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        return destination

    def move_file(self, source, destination):
        source = Path(source).resolve()
        if not source.is_file():
            raise FileNotFoundError(source)
        destination = self.resolve(destination)
        if destination == source:
            raise ValueError("Source and destination are identical")
        if destination.exists():
            raise FileExistsError(destination)

        # A move inside the same storage does not consume additional space.
        try:
            source.relative_to(self.root)
            source_inside_storage = True
        except ValueError:
            source_inside_storage = False

        if not source_inside_storage and not self.can_add(source.stat().st_size):
            raise OSError("Storage limit exceeded")

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
        return destination

    def exists(self, relative_path):
        return self.resolve(relative_path).exists()

    def is_file(self, relative_path):
        return self.resolve(relative_path).is_file()

    def is_dir(self, relative_path):
        return self.resolve(relative_path).is_dir()
