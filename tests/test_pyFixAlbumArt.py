import importlib.machinery
import importlib.util
import tempfile
import unittest
from pathlib import Path

from PIL import Image

loader = importlib.machinery.SourceFileLoader(
    "pyFixAlbumArt",
    str(Path(__file__).resolve().parents[1] / "bin" / "pyFixAlbumArt"),
)
spec = importlib.util.spec_from_loader("pyFixAlbumArt", loader)
module = importlib.util.module_from_spec(spec)
loader.exec_module(module)


class FixAlbumArtTests(unittest.TestCase):
    def test_scan_and_filter_folder_images_returns_large_images(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            album_dir = root / "Album"
            album_dir.mkdir()
            image_path = album_dir / "Folder.jpg"
            image = Image.new("RGB", (600, 600), color="red")
            image.save(image_path, format="JPEG")

            selected = list(module.scan_and_filter_folder_images(start_path=root, size_threshold=1))

            self.assertEqual(selected, [image_path])

    def test_reduce_folder_image_size_rejects_non_folder_names(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            image_path = Path(tmp_dir) / "cover.jpg"
            image_path.write_bytes(b"not-a-real-image")

            with self.assertRaises(ValueError):
                module.reduce_folder_image_size(image_path)

    def test_reduce_folder_image_size_creates_backup_and_replaces_image(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            image_path = Path(tmp_dir) / "Folder.jpg"
            Image.new("RGB", (200, 200), color="blue").save(image_path, format="JPEG")

            result = module.reduce_folder_image_size(image_path, size_threshold=1000000)

            self.assertEqual(result, image_path)
            self.assertTrue(image_path.exists())
            self.assertTrue((Path(tmp_dir) / "Folder-original.jpg").exists())
            self.assertEqual(image_path.suffix, ".jpg")


if __name__ == "__main__":
    unittest.main()
