class FileSize:

    UNITS = ("B", "KB", "MB", "GB", "TB", "PB")

    @classmethod
    def format(cls, size: int) -> str:
        value = float(size)

        for unit in cls.UNITS:
            if value < 1024 or unit == cls.UNITS[-1]:
                return f"{value:.1f} {unit}"
            value /= 1024

        return "0 B"
