from pathlib import Path

from modules.file_model import FileModel


class FileLoader:

    def __init__(self):
        self.folder = Path.home()

    def load(self, path=None) -> list[dict]:

        if path is not None:
            self.folder = Path(path)

        return FileModel(
            self.folder
        ).load()

    def refresh(self) -> list[dict]:
        return self.load(self.folder)
