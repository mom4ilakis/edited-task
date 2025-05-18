import os
from pathlib import Path

SCREENSHOTS_FOLDER = Path(os.environ.get("SCREENSHOTS_FOLDER", "screenshots"))
DB_FILE_FOLDER = Path(os.environ.get("DB_FILE_FOLDER", "db"))
