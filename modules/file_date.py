from datetime import datetime


class FileDate:

    FORMAT = "%d.%m.%Y %H:%M"

    @classmethod
    def format(cls, timestamp: float) -> str:
        return datetime.fromtimestamp(timestamp).strftime(cls.FORMAT)
