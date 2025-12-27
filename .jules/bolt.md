## 2024-05-23 - [EXIF Date Caching]
**Learning:** `functools.lru_cache` on instance methods can cause memory leaks if `self` is part of the cache key and the instance is long-lived or frequently recreated.
**Action:** Use `@staticmethod` for cached methods if they don't rely on instance state, or use a cache attached to the instance, or ensure `maxsize` is bounded. In this case, switching to `@staticmethod` and `@lru_cache(maxsize=1024)` solved the performance bottleneck (4.9x speedup) safely.
