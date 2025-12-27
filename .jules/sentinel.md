## 2024-12-24 - CSV Injection Prevention
**Vulnerability:** CSV Formula Injection (CSV Injection) in image path and date fields. Malicious filenames or data starting with =, +, -, or @ can execute formulas in spreadsheet software.
**Learning:** Even simple file listings can be vulnerable if exported to CSV without sanitization. The vulnerability arises not just from user input but from file system content which can be manipulated.
**Prevention:** Sanitize all fields written to CSV by prepending a single quote (') if they start with risky characters.
