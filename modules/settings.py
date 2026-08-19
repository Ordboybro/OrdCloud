import json
from pathlib import Path


class Settings:
    FILE = Path("data/settings.json")

    DEFAULT = {
        "theme": "dark",
        "language": "ru",
        "view": "list",
        "animations": True,
        "sidebar": True,
        "confirm_delete": True,
        "show_extensions": True,
    }

    def __init__(self):
        self.FILE.parent.mkdir(parents=True, exist_ok=True)
        if not self.FILE.exists():
            self.save(self.DEFAULT)

    def load(self) -> dict:
        try:
            data = json.loads(self.FILE.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("settings must be an object")
            return {**self.DEFAULT, **data}
        except (json.JSONDecodeError, OSError, ValueError):
            return self.DEFAULT.copy()

    def save(self, data: dict) -> None:
        payload = {**self.DEFAULT, **data}
        temporary = self.FILE.with_suffix(".tmp")
        temporary.write_text(
            json.dumps(payload, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )
        temporary.replace(self.FILE)

    def get(self, key: str, default=None):
        return self.load().get(key, default)

    def set(self, key: str, value) -> None:
        data = self.load()
        data[key] = value
        self.save(data)
