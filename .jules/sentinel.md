## 2024-10-27 - CSV Injection in Image Paths
**Vulnerability:** The application writes user-controlled image paths directly to a CSV file. If a folder or file name starts with characters like `=`, `@`, `+`, or `-`, it can be interpreted as a formula by spreadsheet software (CSV Injection / Formula Injection).
**Learning:** Even in desktop applications that deal with local files, inputs like file paths can be vectors for injection attacks if the output format (CSV) is consumed by vulnerable software (Excel).
**Prevention:** Sanitize all string fields written to CSVs by prepending a single quote `'` if they start with dangerous characters. This forces the spreadsheet software to treat the cell content as text.
