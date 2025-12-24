import unittest
import os
import shutil
import csv
from applicationLogic import ApplicationLogic


class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.logic = ApplicationLogic()
        self.test_dir = "=test_security_dir"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_csv_injection_prevention(self):
        # Create a dummy image file in a directory that starts with '='
        malicious_filename = "image.jpg"
        malicious_path = os.path.join(self.test_dir, malicious_filename)
        with open(malicious_path, 'wb') as f:
            f.write(
                b'\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xFF\xDB')

        csv_path = os.path.join(self.test_dir, "output.csv")
        self.logic.writeCSV(csv_path, self.test_dir)

        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            row = next(reader)

            # The path should be sanitized (prepended with ')
            img_path_in_csv = row[0]
            self.assertTrue(
                img_path_in_csv.startswith("'="),
                f"Image path should be sanitized. Got: {img_path_in_csv}")

    def test_sanitize_method(self):
        self.assertEqual(self.logic.sanitize_for_csv("=1+1"), "'=1+1")
        self.assertEqual(self.logic.sanitize_for_csv("+1+1"), "'+1+1")
        self.assertEqual(self.logic.sanitize_for_csv("-1+1"), "'-1+1")
        self.assertEqual(self.logic.sanitize_for_csv("@1+1"), "'@1+1")
        self.assertEqual(self.logic.sanitize_for_csv("Normal"), "Normal")
        self.assertEqual(self.logic.sanitize_for_csv(""), "")
        self.assertEqual(self.logic.sanitize_for_csv(None), None)


if __name__ == '__main__':
    unittest.main()
