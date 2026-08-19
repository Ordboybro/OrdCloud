from pathlib import Path


class Search:
    """Case-insensitive, storage-safe filesystem name search."""

    @staticmethod
    def find(folder: str | Path, text: str) -> list[Path]:
        folder = Path(folder)
        query = text.strip().casefold()
        if not query or not folder.is_dir():
            return []

        result = []
        try:
            for item in folder.rglob("*"):
                try:
                    if item.is_symlink():
                        continue
                    if query in item.name.casefold():
                        result.append(item)
                except OSError:
                    continue
        except (PermissionError, OSError):
            pass

        return result
