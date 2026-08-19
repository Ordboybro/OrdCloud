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
        with self.assertRaises(ValueError):
            self.storage.resolve(self.root)

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
        self.assertEqual(self.storage.get_usage_percent(), 100.0)

    def test_cannot_delete_root(self):
        with self.assertRaises(ValueError):
            self.storage.delete("")

    def test_copy_file_rejects_existing_destination(self):
        source = self.root / "source.txt"
        source.write_text("hello", encoding="utf-8")
        destination = self.root / "copy.txt"
        destination.write_text("existing", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            self.storage.copy_file(source, "copy.txt")

    def test_move_inside_storage_does_not_require_extra_capacity(self):
        source = self.root / "source.txt"
        source.write_bytes(b"x" * 1024)
        destination = self.root / "folder" / "moved.txt"
        destination.parent.mkdir()
        moved = self.storage.move_file(source, destination)
        self.assertEqual(moved, destination.resolve())
        self.assertFalse(source.exists())
        self.assertTrue(destination.exists())
        self.assertEqual(self.storage.get_size(), 1024)

    def test_invalid_names_are_rejected(self):
        with self.assertRaises(ValueError):
            self.storage.create_folder("", "../bad")
        self.storage.create_folder("", "Good")
        with self.assertRaises(ValueError):
            self.storage.rename("Good", "../bad")


if __name__ == "__main__":
    unittest.main()
