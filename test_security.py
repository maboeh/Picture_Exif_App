import unittest
import os
import csv
import shutil
from applicationLogic import ApplicationLogic

class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.vuln_dir = '=vulnerable_folder'
        if os.path.exists(self.vuln_dir):
            shutil.rmtree(self.vuln_dir)
        os.makedirs(self.vuln_dir)
        self.logic = ApplicationLogic()

    def tearDown(self):
        if os.path.exists(self.vuln_dir):
            shutil.rmtree(self.vuln_dir)
        if os.path.exists('output_security.csv'):
            os.remove('output_security.csv')

    def test_csv_injection_mitigation(self):
        """Test that file paths starting with injection characters are sanitized."""
        # Create a dummy image file inside the vulnerable folder
        image_name = 'test.jpg'
        image_path = os.path.join(self.vuln_dir, image_name)

        # Write minimal valid JPEG header
        with open(image_path, 'wb') as f:
             f.write(b'\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00')

        csv_path = 'output_security.csv'
        self.logic.writeCSV(csv_path, self.vuln_dir)

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            row = next(reader)

            written_path = row[0]
            # Verify the path is sanitized (prepended with ')

            self.assertTrue(written_path.startswith("'"), f"Path '{written_path}' should be sanitized (start with ')")

            # Construct the expected sanitized string safely
            # Note: sanitize_for_csv prepends ' to the string representation of the path
            expected_unsanitized = os.path.join(self.vuln_dir, image_name)
            expected_sanitized = f"'{expected_unsanitized}"

            self.assertEqual(written_path, expected_sanitized)

if __name__ == '__main__':
    unittest.main()
