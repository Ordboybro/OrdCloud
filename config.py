from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

APP_NAME = "OrdCloud"
APP_VERSION = "0.7.0"

RESOURCES_DIR = BASE_DIR / "resources"
ICONS_DIR = RESOURCES_DIR / "icons"
IMAGES_DIR = RESOURCES_DIR / "images"
DATA_DIR = BASE_DIR / "data"
STORAGE_DIR = DATA_DIR / "storage"
THEME = RESOURCES_DIR / "style.qss"

# Reference image viewport. Qt scales this naturally on smaller displays.
WINDOW_WIDTH = 1536
WINDOW_HEIGHT = 1024
MIN_WINDOW_WIDTH = 1180
MIN_WINDOW_HEIGHT = 760

MAX_STORAGE_GB = 5
MAX_STORAGE_BYTES = MAX_STORAGE_GB * 1024 * 1024 * 1024

for directory in (RESOURCES_DIR, ICONS_DIR, IMAGES_DIR, DATA_DIR, STORAGE_DIR):
    directory.mkdir(parents=True, exist_ok=True)

DEFAULT_FOLDERS = ("Documents", "Images", "Videos", "Presentations", "Archives")
for folder in DEFAULT_FOLDERS:
    (STORAGE_DIR / folder).mkdir(parents=True, exist_ok=True)
