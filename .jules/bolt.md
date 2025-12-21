## 2024-02-14 - Redundant File I/O in Sort + Process Patterns
**Learning:** In workflows where data is sorted by a property derived from file content (e.g., EXIF date) and then processed (e.g., written to CSV), the expensive derivation function is often called twice: once for the sort key and once for the processing. This doubles the I/O cost.
**Action:** When sorting by an expensive property that will be used again immediately, memoize the property extractor (e.g., using `@lru_cache` on a static method) to eliminate the redundant I/O.
