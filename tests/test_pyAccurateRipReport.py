import contextlib
import importlib.machinery
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

loader = importlib.machinery.SourceFileLoader(
    "pyAccurateRipReport",
    str(Path(__file__).resolve().parents[1] / "bin" / "pyAccurateRipReport"),
)
spec = importlib.util.spec_from_loader("pyAccurateRipReport", loader)
module = importlib.util.module_from_spec(spec)
loader.exec_module(module)


class AccurateRipReportTests(unittest.TestCase):
    def make_track(self, disc_number, accuraterip, secure, track_number=1):
        return module.TrackMetadata(
            album_artist="Artist",
            album="Album",
            artist="Artist",
            date=None,
            disc_number=disc_number,
            disc_total=2,
            encoded_by=None,
            encoder=None,
            genre=None,
            track_name=f"Track {track_number}",
            track_number=track_number,
            track_total=1,
            accuraterip=accuraterip,
            secure=secure,
            ar_confidence=0,
        )

    def test_version_option_prints_script_version(self):
        stream = io.StringIO()

        with contextlib.redirect_stdout(stream):
            with self.assertRaises(SystemExit) as cm:
                module.parse_arguments(["--version"])

        self.assertEqual(cm.exception.code, 0)
        self.assertEqual(stream.getvalue().strip(), f"pyAccurateRipReport {module.VERSION}")

    def test_process_track_metadata_reports_elapsed_time(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            stream = io.StringIO()

            with contextlib.redirect_stdout(stream):
                collection = module.process_track_metadata(Path(tmpdir))

        self.assertEqual(collection, {})
        self.assertIn("Processed 0 tracks", stream.getvalue())
        self.assertIn("seconds", stream.getvalue())

    def test_count_discs_counts_each_disc_in_multi_disc_album(self):
        collection = {
            "Artist": {
                "Album": {
                    1: [self.make_track(1, "accurate", "yes")],
                    2: [self.make_track(2, "inaccurate", "warn")],
                }
            }
        }

        self.assertEqual(module.count_discs(collection), 2)

    def test_good_and_warning_discs_are_classified_by_disc(self):
        collection = {
            "Artist": {
                "Album": {
                    1: [self.make_track(1, "accurate", None)],
                    2: [self.make_track(2, "inaccurate", "warn")],
                }
            }
        }

        good_discs = module.get_good_discs(collection)
        warning_discs = module.get_warning_discs(collection)

        self.assertIn(1, good_discs["Artist"]["Album"])
        self.assertIn(2, warning_discs["Artist"]["Album"])

    def test_good_and_bad_discs_are_classified_separately(self):
        collection = {
            "Artist": {
                "Album": {
                    1: [self.make_track(1, "accurate", None)],
                    2: [self.make_track(2, "inaccurate", "no")],
                }
            }
        }

        good_discs = module.get_good_discs(collection)
        bad_discs = module.get_bad_discs(collection)

        self.assertIn(1, good_discs["Artist"]["Album"])
        self.assertIn(2, bad_discs["Artist"]["Album"])

    def test_mixed_status_disc_is_not_reported_as_perfect(self):
        collection = {
            "Artist": {
                "Album": {
                    1: [
                        self.make_track(1, "accurate", None),
                        self.make_track(1, "inaccurate", "warn", track_number=2),
                    ],
                }
            }
        }

        accurate_discs = module.get_accurate_discs(collection)

        self.assertEqual(accurate_discs, {})

    def test_parse_vorbis_comments_parses_secure_and_accurate_statuses(self):
        sample_text = """
comment[0]: ALBUMARTIST=Artist
comment[1]: ALBUM=Album
comment[2]: TITLE=Song
comment[3]: DISCNUMBER=1
comment[4]: DISCTOTAL=1
comment[5]: TRACKNUMBER=1
comment[6]: TRACKTOTAL=1
comment[7]: ACCURATERIPRESULT=AccurateRip: accurate Secure: yes (warn)
""".strip()

        metadata = module.parse_vorbis_comments(sample_text)

        self.assertEqual(metadata.album_artist, "Artist")
        self.assertEqual(metadata.album, "Album")
        self.assertEqual(metadata.track_name, "Song")
        self.assertEqual(metadata.accuraterip, "accurate")
        self.assertEqual(metadata.secure, "warn")
        self.assertTrue(module.track_is_good(metadata))


if __name__ == "__main__":
    unittest.main()
