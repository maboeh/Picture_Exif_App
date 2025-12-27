## 2024-05-22 - Performance Pattern: functools.lru_cache on class methods
**Learning:** When applying `functools.lru_cache` to class methods, convert them to `@staticmethod` where possible to avoid memory leaks related to the `self` instance and to ensure cache persistence across object lifecycles.
**Action:** Identify stateless instance methods that are computationally expensive or IO-bound and convert them to cached static methods.
