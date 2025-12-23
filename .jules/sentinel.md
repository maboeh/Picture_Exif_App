## 2024-05-23 - CSV Injection (Formula Injection)
**Vulnerability:** The application wrote user-controlled data (filenames) directly to a CSV file. If a file was named starting with `=`, `+`, `-`, or `@`, spreadsheet software (Excel, LibreOffice) would execute it as a formula.
**Learning:** Even desktop applications are vulnerable to CSV injection if they export data that might be opened in spreadsheet software. Filenames are user input.
**Prevention:** Sanitize all fields written to CSVs by prepending `'` if they start with dangerous characters.
