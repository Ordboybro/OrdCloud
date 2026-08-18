from pathlib import Path

from modules.file_date import FileDate
from modules.file_icons import FileIcons
from modules.file_size import FileSize


class FileModel:

    def __init__(self, folder: str | Path):
        self.folder = Path(folder)

    def load(self) -> list[dict]:
        if not self.folder.exists():
            return []

        if not self.folder.is_dir():
            return []

        result = []

        try:
            items = list(self.folder.iterdir())
        except (PermissionError, OSError):
            return []

        items.sort(
            key=lambda item: (
                not item.is_dir(),
                item.name.lower(),
            )
        )

        for item in items:
            try:
                stat = item.stat()

                is_dir = item.is_dir()
                size = 0 if is_dir else stat.st_size

                result.append(
                    {
                        "name": item.name,
                        "icon": FileIcons.emoji(item),
                        "icon_name": FileIcons.name(item),
                        "size": "—" if is_dir else FileSize.format(size),
                        "bytes": size,
                        "modified": FileDate.format(stat.st_mtime),
                        "timestamp": stat.st_mtime,
                        "path": str(item),
                        "dir": is_dir,
                    }
                )

            except (PermissionError, OSError):
                continue

        return result
