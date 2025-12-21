Sentinel Journal

## 2025-12-21 - [CSV Injection Vulnerability]
**Vulnerability:** User-controlled filenames or directory names starting with =, @, +, or - could be executed as formulas when opening the generated CSV in spreadsheet software.
**Learning:** Even when using the standard `csv` module, formula injection is possible because it's a feature of the spreadsheet software, not the CSV format itself.
**Prevention:** Always sanitize data written to CSVs by prepending a single quote (') if the value starts with dangerous characters.
