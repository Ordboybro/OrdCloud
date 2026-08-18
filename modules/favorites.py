import json
from pathlib import Path

from config import DATA_DIR


class Favorites:
    FILE = DATA_DIR / "favorites.json"

    def __init__(self):
        self.FILE.parent.mkdir(parents=True, exist_ok=True)
        if not self.FILE.exists():
            self.save([])

    def load(self) -> list[str]:
        try:
            data = json.loads(self.FILE.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def save(self, data: list[str]) -> None:
        self.FILE.write_text(
            json.dumps(data, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

    def add(self, path: str) -> None:
        data = self.load()
        if path not in data:
            data.append(path)
            self.save(data)

    def remove(self, path: str) -> None:
        data = self.load()
        if path in data:
            data.remove(path)
            self.save(data)

    def contains(self, path: str) -> bool:
        return path in self.load()
