from pathlib import Path
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from delete_empty_files import delete_empty_files
from extract_pdcode import extract_folder, process_pdcode, validate_record
from regex_extractor import extract_patterns
from validate_pd_code_list import validate_file


class MaintenanceTests(unittest.TestCase):
    def test_all_committed_records_validate(self):
        data = Path(__file__).resolve().parents[1] / "data" / "pd_code_list.txt"
        self.assertEqual(validate_file(data), 1424)

    def test_extracts_one_valid_sample(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "L2a1.txt"
            source.write_text("PD[X 1 2 3 4 X 3 4 1 2]", encoding="utf-8")
            self.assertEqual(
                extract_folder(directory),
                [("L2a1", [[1, 2, 3, 4], [3, 4, 1, 2]])],
            )

    def test_rejects_ambiguous_or_bad_pd_blocks(self):
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            process_pdcode("X10111213")
        with self.assertRaisesRegex(ValueError, "occur exactly twice"):
            validate_record("L2a1", [[1, 2, 3, 4], [1, 2, 3, 5]])

    def test_url_extraction_is_unique_and_sorted(self):
        with tempfile.TemporaryDirectory() as directory:
            html = Path(directory) / "index.html"
            html.write_text(
                '"/wiki/L3a2" x "/wiki/L2a1" y "/wiki/L3a2"',
                encoding="utf-8",
            )
            self.assertEqual(extract_patterns(html), ["/wiki/L2a1", "/wiki/L3a2"])

    def test_empty_file_cleanup_skips_hidden_and_nonempty_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            empty = root / "empty.txt"
            empty.write_text(" \n", encoding="utf-8")
            hidden = root / ".keep"
            hidden.write_text("", encoding="utf-8")
            full = root / "full.txt"
            full.write_text("data", encoding="utf-8")
            self.assertEqual(delete_empty_files(root), [empty])
            self.assertTrue(hidden.exists())
            self.assertTrue(full.exists())


if __name__ == "__main__":
    unittest.main()
