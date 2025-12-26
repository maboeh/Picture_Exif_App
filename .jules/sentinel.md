## 2024-05-22 - CSV Injection Vulnerability
**Vulnerability:** The application was vulnerable to CSV Injection (Formula Injection) because it wrote user-controlled filenames and paths directly to a CSV file without sanitization. An attacker could name a file or directory starting with `=`, `@`, `+`, or `-` to execute formulas in Excel when the CSV is opened.
**Learning:** Even local file paths can be vectors for injection attacks if the output format (like CSV) has interpreted semantics. Defensive coding requires sanitizing all untrusted input before export.
**Prevention:** Implemented a `sanitize_for_csv` method that prepends a single quote `'` to any value starting with dangerous characters, forcing Excel to treat it as text. Applied this sanitization to all fields written to the CSV.
