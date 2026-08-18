from pathlib import Path


class Theme:

    @staticmethod
    def load(path: str | Path) -> str:

        path = Path(path)

        if not path.exists():
            return ""

        return path.read_text(
            encoding="utf-8"
        )
