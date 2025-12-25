## 2024-05-23 - Prevent CSV Injection
**Vulnerability:** User-controlled input (filenames and folders) was written directly to CSV files without sanitization. If a filename started with `=`, `@`, `+`, or `-`, it could be interpreted as a formula by spreadsheet software, leading to potential command execution or data exfiltration.
**Learning:** `csv.writer` handles delimiter escaping but does not prevent formula injection. Explicit sanitization is required.
**Prevention:** Implemented `sanitize_for_csv` method that prepends `'` to values starting with dangerous characters. Applied this to all fields in `writeCSV` and `writeCSVSub`.
