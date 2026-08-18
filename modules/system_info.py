import psutil


class SystemInfo:

    @staticmethod
    def disk():
        return psutil.disk_usage("/")

    @staticmethod
    def ram():
        return psutil.virtual_memory()

    @staticmethod
    def cpu():
        return psutil.cpu_percent(
            interval=None
        )
