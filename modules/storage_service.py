from pathlib import Path

from config import (
    STORAGE_DIR,
    MAX_STORAGE_BYTES,
)

from modules.storage import StorageManager


storage = StorageManager(
    root=STORAGE_DIR,
    max_bytes=MAX_STORAGE_BYTES,
)


def storage_path():

    return STORAGE_DIR


def storage_manager():

    return storage


def storage_usage():

    return storage.get_size()


def storage_free():

    return storage.get_free()


def storage_percent():

    return storage.get_usage_percent()
