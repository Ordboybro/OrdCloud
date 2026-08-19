from pathlib import Path

from PySide6.QtCore import QObject, QRunnable, Signal


class SearchSignals(QObject):
    finished = Signal(int, list)


class SearchWorker(QRunnable):
    """Search the current folder tree without blocking the Qt UI thread."""

    def __init__(self, root: Path, needle: str, request_id: int, limit: int = 2000):
        super().__init__()
        self.root = Path(root)
        self.needle = needle.casefold()
        self.request_id = request_id
        self.limit = limit
        self.signals = SearchSignals()
        self.setAutoDelete(True)

    def run(self):
        results = []
        try:
            for path in self.root.rglob("*"):
                if self.needle not in path.name.casefold():
                    continue
                results.append(path)
                if len(results) >= self.limit:
                    break
        except (PermissionError, OSError):
            pass

        results.sort(key=lambda item: (not item.is_dir(), item.name.casefold()))
        self.signals.finished.emit(self.request_id, results)
