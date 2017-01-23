"""db module unittests."""

import unittest
import tempfile
import mock

import db

CSV_DATA = """
"session_id","started_by","created_at","summary_status","duration","worker_time","bundle_time","num_workers","branch","commit_id","started_tests_count","passed_tests_count","failed_tests_count","pending_tests_count","skipped_tests_count","error_tests_count"\n
"934929","wkj@tddium.com","2014-09-01 18:13:35 UTC","passed","528.0","12672.0","0","24","production","97d4b41d9b04af1e6d8a0f19e84af6a448944e46","0","311","0","3","0","0"\n
"934293","wkj@tddium.com","2014-08-31 17:19:26 UTC","failed","479.0","11496.0","0","24","production","fa87080e7d11aad57aa1dcdd82167844e92cc81e","0","310","1","3","0","0"\n
"934046","wkj@tddium.com","2014-08-30 03:18:20 UTC","passed","550.0","13200.0","0","24","production","d4b7952bd576dacc3da52baba1a33dc94f6274e4","0","311","0","3","0","0"\n
"""


class DbTestCase(unittest.TestCase):

    def setUp(self):
        self.csv_file = tempfile.TemporaryFile()
        self.csv_file.write(CSV_DATA)

    def tearDown(self):
        self.csv_file.close()

    def test_build_history(self):
        self.assertTrue(type(db.build_history) is list)

    def test_time_durations(self):
        self.assertTrue(type(db.time_duration) is list)

    def test_create_table(self):
        db.cursor = mock.Mock()
        db.load_data_from_csv(db.FILE_NAME)
        self.assertTrue(db.cursor.execute.called)
        self.assertTrue(db.cursor.executemany.called)
        self.assertEqual(db.cursor.execute.call_count, 1)

    def test_select_statuses(self):
        db.cursor = mock.MagicMock()
        db.get_statuses_by_day()
        self.assertTrue(db.cursor.execute.called)
        self.assertEqual(db.cursor.execute.call_count, 2)

    def test_select_durations(self):
        db.cursor = mock.MagicMock()
        db.get_duration_by_time()
        self.assertTrue(db.cursor.execute.called)
        self.assertEqual(db.cursor.execute.call_count, 1)

if __name__ == '__main__':
    unittest.main()
