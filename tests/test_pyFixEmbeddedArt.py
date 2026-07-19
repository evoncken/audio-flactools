import importlib.machinery
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

loader = importlib.machinery.SourceFileLoader(
    "pyFixEmbeddedArt",
    str(Path(__file__).resolve().parents[1] / "bin" / "pyFixEmbeddedArt"),
)
spec = importlib.util.spec_from_loader("pyFixEmbeddedArt", loader)
module = importlib.util.module_from_spec(spec)
loader.exec_module(module)


class ReplaceEmbeddedPictureTests(unittest.TestCase):
    def test_replace_embedded_picture_raises_for_missing_folder_jpg(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            flac_path = Path(tmp_dir) / "sample.flac"
            flac_path.write_bytes(b"not-a-real-flac")

            with self.assertRaises(FileNotFoundError) as ctx:
                module.replace_embedded_picture(flac_path)

            self.assertIn("Folder.jpg", str(ctx.exception))

    def test_replace_embedded_picture_raises_on_metaflac_failure(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            flac_path = Path(tmp_dir) / "sample.flac"
            flac_path.write_bytes(b"not-a-real-flac")
            folder_jpg = Path(tmp_dir) / "Folder.jpg"
            folder_jpg.write_bytes(b"fake-image")

            with patch.object(module.subprocess, "run", side_effect=subprocess.CalledProcessError(1, ["metaflac"], stderr="boom")):
                with self.assertRaises(subprocess.CalledProcessError):
                    module.replace_embedded_picture(flac_path)


if __name__ == "__main__":
    unittest.main()
