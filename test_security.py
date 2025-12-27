import os
import csv
from applicationLogic import ApplicationLogic

# Subclass to mock behavior without needing actual files
class TestLogic(ApplicationLogic):
    def getPicPaths(self, source_folder):
        # Mocking finding a malicious file
        self.images = ["=cmd|' /C calc'!A0.jpg", "normal.jpg"]

    def get_exif_date(self, image_path):
        return None

def test_csv_injection():
    logic = TestLogic()
    csv_path = "test_output.csv"

    # We don't need a real source folder because we mocked getPicPaths
    logic.writeCSV(csv_path, "dummy_folder")

    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        row1 = next(reader)
        row2 = next(reader)

        print(f"Row 1: {row1}")

        # Check if the malicious payload is unescaped
        if row1[0].startswith("=cmd"):
            print("VULNERABILITY CONFIRMED: Malicious payload written directly to CSV.")
        elif row1[0].startswith("'=cmd"):
            print("FIX VERIFIED: Malicious payload is escaped.")
        else:
            print(f"Unexpected output: {row1[0]}")

if __name__ == "__main__":
    test_csv_injection()
