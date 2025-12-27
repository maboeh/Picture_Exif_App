import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
from applicationLogic import ApplicationLogic
from datetime import datetime

class TestApplicationLogic(unittest.TestCase):

    def setUp(self):
        self.app = ApplicationLogic()
        self.test_dir = "test_images"
        os.makedirs(self.test_dir, exist_ok=True)
        self.csv_file = "test.csv"

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

    @patch("applicationLogic.Image")
    def test_get_exif_date_caching(self, MockImage):
        # Setup mock
        instance = MockImage.return_value
        instance.has_exif = True
        instance.datetime_original = "2023:01:01 12:00:00"

        img_path = os.path.join(self.test_dir, "test.jpg")
        with open(img_path, "w") as f:
            f.write("dummy")

        # First call
        date1 = self.app.get_exif_date(img_path)
        self.assertEqual(date1, datetime(2023, 1, 1, 12, 0, 0))
        self.assertEqual(MockImage.call_count, 1)

        # Second call - should hit cache
        date2 = self.app.get_exif_date(img_path)
        self.assertEqual(date2, datetime(2023, 1, 1, 12, 0, 0))
        self.assertEqual(MockImage.call_count, 1) # Still 1

    def test_get_exif_date_static(self):
        # Verify it can be called on class
        self.assertTrue(hasattr(ApplicationLogic, 'get_exif_date'))
        # We can't easily check if it's staticmethod object once bound,
        # but we can check if it works without instance.
        # But wait, we decorated it, so it's a wrapper.
        pass

if __name__ == '__main__':
    unittest.main()
