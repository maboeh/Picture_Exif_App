## 2024-05-22 - Static Method Caching
**Learning:** When using `@lru_cache` on class methods, it is crucial to convert them to `@staticmethod` if they don't access instance state. This prevents `self` from being part of the cache key, which ensures cache hits even if the method is called from different instances (or if the instance is recreated), and avoids potential memory leaks by keeping the instance alive in the cache.
**Action:** Always check if a method to be cached can be made static. Use `@staticmethod` before `@lru_cache`.
