
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import os
from applicationLogic import ApplicationLogic
import builtins

# Create a mock for exif.Image
class MockImage:
    def __init__(self, file_obj):
        self.has_exif = True
        self.datetime_original = "2023:01:01 12:00:00"

class TestPerformanceOptimized(unittest.TestCase):
    def setUp(self):
        # Clear lru_cache before each test to ensure fresh start
        ApplicationLogic.get_exif_date.cache_clear()

        self.app = ApplicationLogic()
        self.source_folder = "/fake/source"
        self.files = [f"image_{i}.jpg" for i in range(100)] # 100 images

    @patch('applicationLogic.Image', side_effect=MockImage)
    @patch('builtins.open', new_callable=MagicMock)
    @patch('os.listdir')
    @patch('os.path.join', side_effect=lambda a, b: f"{a}/{b}")
    @patch('os.path.exists', return_value=True)
    def test_optimization(self, mock_exists, mock_join, mock_listdir, mock_open, mock_image):
        # Mock os.listdir
        mock_listdir.return_value = self.files

        # Mock open context manager
        file_handle = MagicMock()
        mock_open.return_value.__enter__.return_value = file_handle

        print("\n--- Testing Optimized Performance ---")

        # 1. First run: should open files N times (cache miss)
        # Note: getPicPaths calls get_exif_date N times for sorting
        self.app.getPicPaths(self.source_folder)

        calls_first_run = mock_open.call_count
        print(f"File opens after first getPicPaths: {calls_first_run}")
        self.assertEqual(calls_first_run, 100, "First run should open all 100 files")

        # Reset mock counts but NOT the cache
        mock_open.reset_mock()

        # 2. Second run: writeCSV calls getPicPaths again + iterates again
        # Should hit cache for all image reads!
        # Only 1 file open allowed (for the CSV file itself)

        with patch('csv.writer'):
            self.app.writeCSV("/fake/target.csv", self.source_folder)

        calls_second_run = mock_open.call_count
        print(f"File opens during writeCSV (cached): {calls_second_run}")

        # Expectation: 0 opens for images, 1 open for CSV = 1 total
        self.assertEqual(calls_second_run, 1, "Should only open the CSV file, images should be cached")

if __name__ == '__main__':
    unittest.main()
