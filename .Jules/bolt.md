## 2024-05-23 - [EXIF Date Caching]
**Learning:** Calling `sorted(list, key=func)` calls `func` exactly once per item, but if you iterate the list later and call `func` again, you double the work.
**Action:** Always look for "Sort then Process" patterns where the sort key is expensive. Use `functools.lru_cache` on the key function (converting to `@staticmethod` if inside a class) to make the second pass instant.
