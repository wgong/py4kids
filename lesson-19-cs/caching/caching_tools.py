"""
Caching Tools Library

A comprehensive library for various caching strategies in Python.
Provides TTL caching, LRU caching, and advanced search functionality.

Author: Generated via Claude Code workflow
Version: 1.0.0
"""

import time
import functools
import threading
import hashlib
import pickle
from typing import Any, Callable, Dict, Tuple, Optional, Union, List
from cachetools import TTLCache, LRUCache, TLRUCache, LFUCache


class TTLCacheSimple:
    """Simple Time-To-Live cache implementation without external dependencies"""
    
    def __init__(self):
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._lock = threading.RLock()
    
    def get(self, key: str, ttl: float) -> Tuple[bool, Any]:
        """Get item from cache if not expired"""
        with self._lock:
            if key in self._cache:
                value, timestamp = self._cache[key]
                if time.time() - timestamp < ttl:
                    return True, value
                else:
                    # Remove expired entry
                    del self._cache[key]
            return False, None
    
    def set(self, key: str, value: Any) -> None:
        """Store item in cache with current timestamp"""
        with self._lock:
            self._cache[key] = (value, time.time())
    
    def clear(self) -> None:
        """Clear all cached items"""
        with self._lock:
            self._cache.clear()
    
    def size(self) -> int:
        """Get number of cached items"""
        with self._lock:
            return len(self._cache)


class HashSearcher:
    """
    Efficient hash-based search with configurable caching strategies.
    
    Provides O(1) lookups by converting arrays to hash maps and caching
    the results to avoid rebuilding for repeated searches.
    """
    
    def __init__(self, cache_type: str = 'ttl', ttl_seconds: int = 300, 
                 maxsize: int = 100, enable_stats: bool = False):
        """
        Initialize HashSearcher with specified caching strategy.
        
        Args:
            cache_type: 'ttl', 'lru', 'tlru', or 'lfu'
            ttl_seconds: Time-to-live for TTL and TLRU caches
            maxsize: Maximum cache size
            enable_stats: Whether to track hit/miss statistics
        """
        self.enable_stats = enable_stats
        self.hit_count = 0
        self.miss_count = 0
        self.cache_type = cache_type
        self._lock = threading.RLock()
        
        # Initialize cache based on type
        if cache_type == 'ttl':
            self._cache = TTLCache(maxsize=maxsize, ttl=ttl_seconds)
        elif cache_type == 'lru':
            self._cache = LRUCache(maxsize=maxsize)
        elif cache_type == 'tlru':
            self._cache = TLRUCache(maxsize=maxsize, ttu=ttl_seconds)
        elif cache_type == 'lfu':
            self._cache = LFUCache(maxsize=maxsize)
        else:
            raise ValueError(f"Unsupported cache type: {cache_type}")
    
    def search(self, array: List[Any], item: Any) -> Optional[int]:
        """
        Search for item in array using cached hash map.
        
        Args:
            array: List to search in
            item: Item to find
            
        Returns:
            Index of item or None if not found
        """
        if array is None or len(array) < 1:
            return None
        
        array_key = self._create_cache_key(array)
        
        with self._lock:
            if array_key not in self._cache:
                if self.enable_stats:
                    self.miss_count += 1
                # Create and cache the hash map
                self._cache[array_key] = {val: n for n, val in enumerate(array)}
            else:
                if self.enable_stats:
                    self.hit_count += 1
            
            hash_map = self._cache[array_key]
        
        return hash_map.get(item)
    
    def _create_cache_key(self, array: List[Any]) -> str:
        """Create a robust cache key for the array"""
        try:
            # Try built-in hash first (fastest for hashable types)
            return str(hash(tuple(array)))
        except TypeError:
            # Fallback for unhashable elements
            array_bytes = pickle.dumps(array)
            return hashlib.md5(array_bytes).hexdigest()
    
    def clear_cache(self) -> None:
        """Clear all cached items"""
        with self._lock:
            self._cache.clear()
    
    def cache_info(self) -> Dict[str, Any]:
        """Get cache statistics and configuration"""
        with self._lock:
            info = {
                'cache_type': self.cache_type,
                'size': len(self._cache),
                'maxsize': getattr(self._cache, 'maxsize', None),
            }
            
            if hasattr(self._cache, 'ttl'):
                info['ttl'] = self._cache.ttl
            if hasattr(self._cache, 'ttu'):
                info['ttu'] = self._cache.ttu
                
            if self.enable_stats:
                info.update({
                    'hit_count': self.hit_count,
                    'miss_count': self.miss_count,
                    'hit_ratio': self.get_hit_ratio()
                })
            
            return info
    
    def get_hit_ratio(self) -> float:
        """Calculate cache hit ratio"""
        total = self.hit_count + self.miss_count
        return self.hit_count / total if total > 0 else 0.0
    
    def contains_array(self, array: List[Any]) -> bool:
        """Check if array is already cached"""
        array_key = self._create_cache_key(array)
        with self._lock:
            return array_key in self._cache


class DataSearchLibrary:
    """
    High-level search library with automatic method selection.
    
    Automatically chooses between linear search (for small arrays) and
    cached hash search (for large arrays) for optimal performance.
    """
    
    def __init__(self, hash_threshold: int = 100, **kwargs):
        """
        Initialize DataSearchLibrary.
        
        Args:
            hash_threshold: Array size threshold for using hash search
            **kwargs: Arguments passed to HashSearcher
        """
        self.hash_threshold = hash_threshold
        self.hash_searcher = HashSearcher(**kwargs)
    
    def find_in_array(self, array: List[Any], item: Any, 
                     method: str = 'auto') -> Optional[int]:
        """
        Find item in array using the best search method.
        
        Args:
            array: List to search in
            item: Item to find
            method: 'hash', 'linear', or 'auto'
        
        Returns:
            Index of item or None if not found
        """
        if array is None or len(array) == 0:
            return None
        
        if method == 'hash' or (method == 'auto' and len(array) >= self.hash_threshold):
            return self.hash_searcher.search(array, item)
        else:
            # Use linear search for small arrays or when explicitly requested
            try:
                return array.index(item)
            except ValueError:
                return None
    
    def batch_search(self, array: List[Any], items: List[Any], 
                    method: str = 'auto') -> Dict[Any, Optional[int]]:
        """
        Perform batch search for multiple items in the same array.
        
        Args:
            array: List to search in
            items: List of items to find
            method: Search method to use
            
        Returns:
            Dictionary mapping items to their indices (or None if not found)
        """
        return {item: self.find_in_array(array, item, method) for item in items}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics"""
        return {
            'hash_threshold': self.hash_threshold,
            'hash_searcher_stats': self.hash_searcher.cache_info()
        }
    
    def clear_caches(self) -> None:
        """Clear all internal caches"""
        self.hash_searcher.clear_cache()


def cache_with_ttl(ttl: float = 3600, hash_func: Optional[Callable] = None):
    """
    Decorator to cache function results with TTL (Time-To-Live).
    
    Args:
        ttl: Time-to-live in seconds (default: 3600 = 1 hour)
        hash_func: Optional custom hash function for cache keys
    
    Usage:
        @cache_with_ttl(ttl=3600)
        def expensive_function(arg1, arg2):
            # Your function implementation
            pass
    """
    # Use global cache for decorator
    _global_cache = TTLCacheSimple()
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            if hash_func:
                cache_key = hash_func(*args, **kwargs)
            else:
                # Default: hash function name + arguments
                key_data = (func.__name__, args, tuple(sorted(kwargs.items())))
                cache_key = hashlib.md5(pickle.dumps(key_data)).hexdigest()
            
            # Try to get from cache
            hit, cached_value = _global_cache.get(cache_key, ttl)
            if hit:
                return cached_value
            
            # Cache miss - call function and store result
            result = func(*args, **kwargs)
            _global_cache.set(cache_key, result)
            return result
        
        # Add cache management methods to the decorated function
        wrapper.clear_cache = lambda: _global_cache.clear()
        wrapper.cache_info = lambda: {
            'cache_size': _global_cache.size(),
            'ttl': ttl
        }
        
        return wrapper
    return decorator


class CacheManager:
    """
    Advanced cache manager for complex applications.
    
    Provides multiple named caches with different strategies and
    centralized management capabilities.
    """
    
    def __init__(self):
        self._caches: Dict[str, Any] = {}
        self._cache_configs: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
    
    def create_cache(self, name: str, cache_type: str = 'ttl', **kwargs) -> Any:
        """
        Create a named cache with specified configuration.
        
        Args:
            name: Unique cache name
            cache_type: Type of cache ('ttl', 'lru', 'tlru', 'lfu')
            **kwargs: Cache-specific configuration
            
        Returns:
            Created cache instance
        """
        with self._lock:
            if name in self._caches:
                raise ValueError(f"Cache '{name}' already exists")
            
            # Create cache based on type
            if cache_type == 'ttl':
                cache = TTLCache(maxsize=kwargs.get('maxsize', 100), 
                               ttl=kwargs.get('ttl', 300))
            elif cache_type == 'lru':
                cache = LRUCache(maxsize=kwargs.get('maxsize', 100))
            elif cache_type == 'tlru':
                cache = TLRUCache(maxsize=kwargs.get('maxsize', 100),
                                 ttu=kwargs.get('ttu', 300))
            elif cache_type == 'lfu':
                cache = LFUCache(maxsize=kwargs.get('maxsize', 100))
            else:
                raise ValueError(f"Unsupported cache type: {cache_type}")
            
            self._caches[name] = cache
            self._cache_configs[name] = {'type': cache_type, **kwargs}
            return cache
    
    def get_cache(self, name: str) -> Any:
        """Get cache by name"""
        with self._lock:
            if name not in self._caches:
                raise KeyError(f"Cache '{name}' not found")
            return self._caches[name]
    
    def clear_cache(self, name: str) -> None:
        """Clear specific cache"""
        cache = self.get_cache(name)
        cache.clear()
    
    def clear_all_caches(self) -> None:
        """Clear all managed caches"""
        with self._lock:
            for cache in self._caches.values():
                cache.clear()
    
    def get_cache_info(self, name: Optional[str] = None) -> Dict[str, Any]:
        """Get information about caches"""
        with self._lock:
            if name:
                if name not in self._caches:
                    raise KeyError(f"Cache '{name}' not found")
                cache = self._caches[name]
                config = self._cache_configs[name]
                return {
                    'name': name,
                    'type': config['type'],
                    'size': len(cache),
                    'maxsize': getattr(cache, 'maxsize', None),
                    'ttl': getattr(cache, 'ttl', None),
                    'ttu': getattr(cache, 'ttu', None),
                    'config': config
                }
            else:
                # Return info for all caches
                return {
                    name: self.get_cache_info(name) 
                    for name in self._caches.keys()
                }
    
    def list_caches(self) -> List[str]:
        """List all cache names"""
        with self._lock:
            return list(self._caches.keys())


# Performance testing utilities
def benchmark_search_methods(array_sizes: List[int], search_counts: List[int] = None) -> Dict[str, Any]:
    """
    Benchmark different search methods across various array sizes.
    
    Args:
        array_sizes: List of array sizes to test
        search_counts: Number of searches per array size (default: [100])
        
    Returns:
        Dictionary with benchmark results
    """
    import time
    import statistics
    
    if search_counts is None:
        search_counts = [100]
    
    results = {}
    
    for size in array_sizes:
        test_array = list(range(size))
        search_item = size // 2  # Search for middle element
        
        size_results = {}
        
        for search_count in search_counts:
            # Test linear search
            start_time = time.time()
            for _ in range(search_count):
                try:
                    test_array.index(search_item)
                except ValueError:
                    pass
            linear_time = time.time() - start_time
            
            # Test cached hash search
            searcher = HashSearcher(cache_type='ttl', enable_stats=True)
            start_time = time.time()
            for _ in range(search_count):
                searcher.search(test_array, search_item)
            hash_time = time.time() - start_time
            
            # Test library auto-selection
            lib = DataSearchLibrary(enable_stats=True)
            start_time = time.time()
            for _ in range(search_count):
                lib.find_in_array(test_array, search_item)
            auto_time = time.time() - start_time
            
            size_results[f"{search_count}_searches"] = {
                'linear_time': linear_time,
                'hash_time': hash_time,
                'auto_time': auto_time,
                'hash_vs_linear_speedup': linear_time / hash_time if hash_time > 0 else float('inf'),
                'hash_cache_stats': searcher.cache_info()
            }
        
        results[f"array_size_{size}"] = size_results
    
    return results


# Example usage and demonstrations
if __name__ == "__main__":
    # Demonstrate basic functionality
    print("=== Caching Tools Demo ===\n")
    
    # 1. Basic HashSearcher
    print("1. HashSearcher with TTL caching:")
    searcher = HashSearcher(cache_type='ttl', ttl_seconds=60, enable_stats=True)
    test_array = [10, 20, 30, 40, 50]
    
    print(f"   Search for 30: {searcher.search(test_array, 30)}")
    print(f"   Search for 40: {searcher.search(test_array, 40)}")
    print(f"   Cache info: {searcher.cache_info()}")
    
    # 2. DataSearchLibrary
    print("\n2. DataSearchLibrary with auto-selection:")
    lib = DataSearchLibrary(hash_threshold=3, enable_stats=True)
    
    small_array = [1, 2, 3]
    large_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    print(f"   Small array (linear): {lib.find_in_array(small_array, 2)}")
    print(f"   Large array (hash): {lib.find_in_array(large_array, 7)}")
    print(f"   Library stats: {lib.get_stats()}")
    
    # 3. Batch search
    print("\n3. Batch search:")
    items_to_find = [1, 3, 5, 7, 11]  # 11 doesn't exist
    batch_results = lib.batch_search(large_array, items_to_find)
    print(f"   Batch results: {batch_results}")
    
    # 4. Cache decorator
    print("\n4. Cache decorator:")
    
    @cache_with_ttl(ttl=5)
    def slow_function(x):
        time.sleep(0.1)  # Simulate slow operation
        return x * x
    
    start = time.time()
    result1 = slow_function(5)  # Should be slow
    first_call_time = time.time() - start
    
    start = time.time()
    result2 = slow_function(5)  # Should be fast (cached)
    second_call_time = time.time() - start
    
    print(f"   First call: {result1} (took {first_call_time:.3f}s)")
    print(f"   Second call: {result2} (took {second_call_time:.3f}s)")
    print(f"   Cache info: {slow_function.cache_info()}")
    
    print("\n=== Demo Complete ===")