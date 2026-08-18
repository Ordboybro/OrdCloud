from pathlib import Path


class Clipboard:

    def __init__(self):
        self.path: Path | None = None
        self.mode: str | None = None

    def copy(self, path: str | Path) -> None:
        self.path = Path(path)
        self.mode = "copy"

    def cut(self, path: str | Path) -> None:
        self.path = Path(path)
        self.mode = "cut"

    def clear(self) -> None:
        self.path = None
        self.mode = None

    def has_data(self) -> bool:
        return self.path is not None and self.mode is not None
