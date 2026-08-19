import tempfile
import unittest
from pathlib import Path

from modules.search import Search
from modules.settings import Settings


class CoreTests(unittest.TestCase):
    def test_search_is_case_and_unicode_insensitive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Презентация.PDF").write_text("x", encoding="utf-8")
            (root / "notes.txt").write_text("x", encoding="utf-8")
            names = {path.name for path in Search.find(root, "ПРЕЗЕН")}
            self.assertEqual(names, {"Презентация.PDF"})

    def test_search_ignores_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root / "outside.txt"
            outside.write_text("secret", encoding="utf-8")
            link = root / "linked.txt"
            try:
                link.symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks are unavailable on this platform")
            self.assertEqual(Search.find(root, "linked"), [])

    def test_settings_have_stable_defaults_and_reset(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = Settings.FILE
            try:
                Settings.FILE = Path(tmp) / "settings.json"
                settings = Settings()
                settings.set("view", "grid")
                self.assertEqual(settings.get("view"), "grid")
                settings.reset()
                self.assertEqual(settings.get("view"), "list")
            finally:
                Settings.FILE = original


if __name__ == "__main__":
    unittest.main()
