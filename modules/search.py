from pathlib import Path


class Search:

    @staticmethod
    def find(
        folder: str | Path,
        text: str,
    ) -> list[Path]:

        folder = Path(folder)

        if not text:
            return []

        text = text.lower()

        result = []

        try:
            for item in folder.rglob("*"):
                if text in item.name.lower():
                    result.append(item)
        except (
            PermissionError,
            OSError,
        ):
            pass

        return result
