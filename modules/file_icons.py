from pathlib import Path


class FileIcons:

    EXTENSIONS = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".html": "html",
        ".css": "css",
        ".json": "json",
        ".xml": "xml",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".md": "markdown",
        ".txt": "text",
        ".log": "text",

        ".pdf": "pdf",
        ".doc": "word",
        ".docx": "word",
        ".xls": "excel",
        ".xlsx": "excel",
        ".ppt": "powerpoint",
        ".pptx": "powerpoint",

        ".png": "image",
        ".jpg": "image",
        ".jpeg": "image",
        ".gif": "image",
        ".webp": "image",
        ".svg": "image",

        ".mp3": "music",
        ".wav": "music",
        ".flac": "music",

        ".mp4": "video",
        ".avi": "video",
        ".mkv": "video",
        ".mov": "video",

        ".zip": "archive",
        ".rar": "archive",
        ".7z": "archive",
        ".tar": "archive",
        ".gz": "archive",

        ".exe": "application",
        ".msi": "application",
    }

    @classmethod
    def name(cls, path: str | Path) -> str:
        path = Path(path)

        if path.is_dir():
            return "folder"

        return cls.EXTENSIONS.get(
            path.suffix.lower(),
            "file",
        )

    @classmethod
    def emoji(cls, path: str | Path) -> str:
        icons = {
            "folder": "📁",
            "python": "🐍",
            "javascript": "🟨",
            "typescript": "🔷",
            "html": "🌐",
            "css": "🎨",
            "json": "⚙️",
            "xml": "⚙️",
            "yaml": "⚙️",
            "markdown": "📝",
            "text": "📄",
            "pdf": "📕",
            "word": "📘",
            "excel": "📗",
            "powerpoint": "📙",
            "image": "🖼️",
            "music": "🎵",
            "video": "🎥",
            "archive": "🗜️",
            "application": "🖥️",
            "file": "📄",
        }

        return icons.get(cls.name(path), "📄")
