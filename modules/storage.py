from pathlib import Path
import shutil


class StorageManager:

    def __init__(self, root: Path, max_bytes: int):
        self.root = Path(root)
        self.max_bytes = max_bytes

        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ---------------------------------------------------------
    # PATH
    # ---------------------------------------------------------

    def resolve(self, relative_path=""):
        relative = Path(relative_path)

        if relative.is_absolute():
            raise ValueError(
                "Absolute paths are not allowed"
            )

        target = (
            self.root / relative
        ).resolve()

        try:
            target.relative_to(
                self.root.resolve()
            )
        except ValueError:
            raise ValueError(
                "Path escapes storage"
            )

        return target

    # ---------------------------------------------------------
    # SIZE
    # ---------------------------------------------------------

    def get_size(self) -> int:

        total = 0

        for path in self.root.rglob("*"):

            try:

                if path.is_file():
                    total += path.stat().st_size

            except (
                OSError,
                PermissionError,
            ):
                continue

        return total

    def get_free(self) -> int:

        return max(
            0,
            self.max_bytes - self.get_size(),
        )

    def get_usage_percent(self) -> float:

        if self.max_bytes <= 0:
            return 0

        return (
            self.get_size()
            / self.max_bytes
            * 100
        )

    # ---------------------------------------------------------
    # LIMIT
    # ---------------------------------------------------------

    def can_add(self, size: int) -> bool:

        return (
            self.get_size() + size
            <= self.max_bytes
        )

    # ---------------------------------------------------------
    # CREATE FOLDER
    # ---------------------------------------------------------

    def create_folder(
        self,
        parent="",
        name="New Folder",
    ):

        if not name.strip():
            raise ValueError(
                "Folder name cannot be empty"
            )

        parent_path = self.resolve(parent)

        target = (
            parent_path / name
        ).resolve()

        target.relative_to(
            self.root.resolve()
        )

        target.mkdir(
            parents=False,
            exist_ok=False,
        )

        return target

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------

    def delete(self, relative_path):

        target = self.resolve(
            relative_path
        )

        if target == self.root:
            raise ValueError(
                "Cannot delete storage root"
            )

        if target.is_dir():

            shutil.rmtree(target)

        elif target.exists():

            target.unlink()

    # ---------------------------------------------------------
    # RENAME
    # ---------------------------------------------------------

    def rename(
        self,
        relative_path,
        new_name,
    ):

        if not new_name.strip():
            raise ValueError(
                "New name cannot be empty"
            )

        target = self.resolve(
            relative_path
        )

        if target == self.root:
            raise ValueError(
                "Cannot rename storage root"
            )

        new_path = (
            target.parent / new_name
        ).resolve()

        new_path.relative_to(
            self.root.resolve()
        )

        if new_path.exists():
            raise FileExistsError(
                "Target already exists"
            )

        target.rename(
            new_path
        )

        return new_path

    # ---------------------------------------------------------
    # COPY FILE
    # ---------------------------------------------------------

    def copy_file(
        self,
        source,
        destination,
    ):

        source = Path(source)

        if not source.is_file():
            raise FileNotFoundError(
                source
            )

        size = source.stat().st_size

        if not self.can_add(size):
            raise OSError(
                "Storage limit exceeded"
            )

        destination = self.resolve(
            destination
        )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(
            source,
            destination,
        )

        return destination

    # ---------------------------------------------------------
    # MOVE FILE
    # ---------------------------------------------------------

    def move_file(
        self,
        source,
        destination,
    ):

        source = Path(source)

        if not source.is_file():
            raise FileNotFoundError(
                source
            )

        size = source.stat().st_size

        if not self.can_add(size):
            raise OSError(
                "Storage limit exceeded"
            )

        destination = self.resolve(
            destination
        )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.move(
            str(source),
            str(destination),
        )

        return destination

    # ---------------------------------------------------------
    # FILE INFO
    # ---------------------------------------------------------

    def exists(self, relative_path):

        return self.resolve(
            relative_path
        ).exists()

    def is_file(self, relative_path):

        return self.resolve(
            relative_path
        ).is_file()

    def is_dir(self, relative_path):

        return self.resolve(
            relative_path
        ).is_dir()
