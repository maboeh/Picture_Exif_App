## 2024-05-23 - CSV Injection in Exports
**Vulnerability:** The application was exporting file paths directly to CSV without sanitization. If a file path started with characters like `=`, `@`, `+`, or `-`, opening the CSV in Excel could execute it as a formula.
**Learning:** Even desktop applications are vulnerable to CSV injection if they export user-controlled data (filenames, metadata) to CSVs intended for spreadsheet software.
**Prevention:** Implemented `sanitize_for_csv` to quote values starting with dangerous characters.
