from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

APP_NAME = "OrdFiles"
APP_VERSION = "0.1.0"

RESOURCES_DIR = BASE_DIR / "resources"
ICONS_DIR = RESOURCES_DIR / "icons"
IMAGES_DIR = RESOURCES_DIR / "images"

DATA_DIR = BASE_DIR / "data"

STORAGE_DIR = DATA_DIR / "storage"

THEME = RESOURCES_DIR / "style.qss"
LIGHT_THEME = RESOURCES_DIR / "light.qss"

WINDOW_WIDTH = 1536
WINDOW_HEIGHT = 1024

MIN_WINDOW_WIDTH = 1100
MIN_WINDOW_HEIGHT = 700

MAX_STORAGE_GB = 5

MAX_STORAGE_BYTES = (
    MAX_STORAGE_GB
    * 1024
    * 1024
    * 1024
)

for directory in (
    RESOURCES_DIR,
    ICONS_DIR,
    IMAGES_DIR,
    DATA_DIR,
    STORAGE_DIR,
):
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )
