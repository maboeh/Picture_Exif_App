
import unittest
from applicationLogic import ApplicationLogic

class TestApplicationLogicSecurity(unittest.TestCase):
    def setUp(self):
        self.app = ApplicationLogic()

    def test_sanitize_for_csv_safe_input(self):
        """Test that safe input is returned unchanged."""
        self.assertEqual(self.app.sanitize_for_csv("normal_filename.jpg"), "normal_filename.jpg")
        self.assertEqual(self.app.sanitize_for_csv("2023-10-27"), "2023-10-27")

    def test_sanitize_for_csv_dangerous_input(self):
        """Test that dangerous input is sanitized."""
        # Starts with =
        self.assertEqual(self.app.sanitize_for_csv("=cmd|' /C calc'!A0"), "'=cmd|' /C calc'!A0")
        # Starts with @
        self.assertEqual(self.app.sanitize_for_csv("@SUM(1,1)"), "'@SUM(1,1)")
        # Starts with +
        self.assertEqual(self.app.sanitize_for_csv("+1+1"), "'+1+1")
        # Starts with -
        self.assertEqual(self.app.sanitize_for_csv("-1+1"), "'-1+1")

    def test_sanitize_for_csv_non_string(self):
        """Test that non-string input is handled gracefully."""
        self.assertEqual(self.app.sanitize_for_csv(123), 123)
        self.assertEqual(self.app.sanitize_for_csv(None), None)

if __name__ == '__main__':
    unittest.main()
