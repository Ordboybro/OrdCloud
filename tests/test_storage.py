import tempfile
import unittest
from pathlib import Path

from modules.storage import StorageManager


class StorageManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name) / "storage"
        self.storage = StorageManager(self.root, 1024)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_resolve_stays_inside_storage(self):
        self.assertEqual(self.storage.resolve("docs"), self.root.resolve() / "docs")
        with self.assertRaises(ValueError):
            self.storage.resolve("../outside")

    def test_create_folder_and_rename(self):
        folder = self.storage.create_folder("", "Documents")
        self.assertTrue(folder.is_dir())
        renamed = self.storage.rename("Documents", "Files")
        self.assertTrue(renamed.is_dir())
        self.assertFalse(folder.exists())

    def test_storage_limit(self):
        file = self.root / "a.bin"
        file.write_bytes(b"x" * 1024)
        self.assertFalse(self.storage.can_add(1))
        self.assertEqual(self.storage.get_size(), 1024)
        self.assertEqual(self.storage.get_free(), 0)

    def test_cannot_delete_root(self):
        with self.assertRaises(ValueError):
            self.storage.delete("")


if __name__ == "__main__":
    unittest.main()
