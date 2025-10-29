"""
Comprehensive Test Suite for Caching Tools Library

Tests all components of the caching_tools module including:
- TTLCacheSimple
- HashSearcher with different cache types
- DataSearchLibrary
- Cache decorators
- CacheManager
- Performance benchmarks

Run with: python -m pytest caching_tools_test.py -v
Or: python caching_tools_test.py
"""

import unittest
import time
import threading
from unittest.mock import patch, MagicMock
from caching_tools import (
    TTLCacheSimple, HashSearcher, DataSearchLibrary, 
    cache_with_ttl, CacheManager, benchmark_search_methods
)


class TestTTLCacheSimple(unittest.TestCase):
    """Test the simple TTL cache implementation"""
    
    def setUp(self):
        self.cache = TTLCacheSimple()
    
    def test_basic_operations(self):
        """Test basic cache operations"""
        # Test empty cache
        hit, value = self.cache.get("key1", 60)
        self.assertFalse(hit)
        self.assertIsNone(value)
        self.assertEqual(self.cache.size(), 0)
        
        # Test set and get
        self.cache.set("key1", "value1")
        self.assertEqual(self.cache.size(), 1)
        
        hit, value = self.cache.get("key1", 60)
        self.assertTrue(hit)
        self.assertEqual(value, "value1")
    
    def test_ttl_expiration(self):
        """Test TTL expiration functionality"""
        self.cache.set("key1", "value1")
        
        # Should be available immediately
        hit, value = self.cache.get("key1", 1.0)  # 1 second TTL
        self.assertTrue(hit)
        self.assertEqual(value, "value1")
        
        # Wait for expiration
        time.sleep(1.1)
        hit, value = self.cache.get("key1", 1.0)
        self.assertFalse(hit)
        self.assertIsNone(value)
        self.assertEqual(self.cache.size(), 0)  # Should be cleaned up
    
    def test_clear_cache(self):
        """Test cache clearing"""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.assertEqual(self.cache.size(), 2)
        
        self.cache.clear()
        self.assertEqual(self.cache.size(), 0)
        
        hit, value = self.cache.get("key1", 60)
        self.assertFalse(hit)
    
    def test_thread_safety(self):
        """Test thread safety of cache operations"""
        def worker(cache, thread_id):
            for i in range(10):
                key = f"key_{thread_id}_{i}"
                cache.set(key, f"value_{thread_id}_{i}")
                hit, value = cache.get(key, 60)
                self.assertTrue(hit)
                self.assertEqual(value, f"value_{thread_id}_{i}")
        
        threads = []
        for i in range(5):
            t = threading.Thread(target=worker, args=(self.cache, i))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        # Should have 50 items (5 threads × 10 items each)
        self.assertEqual(self.cache.size(), 50)


class TestHashSearcher(unittest.TestCase):
    """Test the HashSearcher class with different cache types"""
    
    def test_basic_search(self):
        """Test basic search functionality"""
        searcher = HashSearcher(cache_type='ttl', enable_stats=True)
        array = [10, 20, 30, 40, 50]
        
        # Test successful search
        result = searcher.search(array, 30)
        self.assertEqual(result, 2)
        self.assertEqual(searcher.miss_count, 1)  # First call is cache miss
        
        # Test cache hit
        result = searcher.search(array, 40)
        self.assertEqual(result, 3)
        self.assertEqual(searcher.hit_count, 1)  # Second call is cache hit
        
        # Test item not found
        result = searcher.search(array, 100)
        self.assertIsNone(result)
    
    def test_different_cache_types(self):
        """Test different cache implementations"""
        cache_types = ['ttl', 'lru', 'tlru', 'lfu']
        array = [1, 2, 3, 4, 5]
        
        for cache_type in cache_types:
            with self.subTest(cache_type=cache_type):
                searcher = HashSearcher(cache_type=cache_type)
                result = searcher.search(array, 3)
                self.assertEqual(result, 2)
                
                # Test cache info
                info = searcher.cache_info()
                self.assertEqual(info['cache_type'], cache_type)
                self.assertEqual(info['size'], 1)
    
    def test_invalid_cache_type(self):
        """Test handling of invalid cache types"""
        with self.assertRaises(ValueError):
            HashSearcher(cache_type='invalid')
    
    def test_edge_cases(self):
        """Test edge cases"""
        searcher = HashSearcher()
        
        # Empty array
        self.assertIsNone(searcher.search([], 1))
        
        # None array
        self.assertIsNone(searcher.search(None, 1))
        
        # Single element
        self.assertEqual(searcher.search([42], 42), 0)
        self.assertIsNone(searcher.search([42], 43))
    
    def test_unhashable_elements(self):
        """Test arrays with unhashable elements"""
        searcher = HashSearcher()
        
        # Array with lists (unhashable)
        array = [[1, 2], [3, 4], [5, 6]]
        result = searcher.search(array, [3, 4])
        self.assertEqual(result, 1)
        
        # Array with dicts (unhashable)
        array = [{'a': 1}, {'b': 2}, {'c': 3}]
        result = searcher.search(array, {'b': 2})
        self.assertEqual(result, 1)
    
    def test_contains_array(self):
        """Test contains_array method"""
        searcher = HashSearcher()
        array = [1, 2, 3, 4, 5]
        
        # Should not be cached initially
        self.assertFalse(searcher.contains_array(array))
        
        # After search, should be cached
        searcher.search(array, 3)
        self.assertTrue(searcher.contains_array(array))
    
    def test_cache_stats(self):
        """Test cache statistics"""
        searcher = HashSearcher(enable_stats=True)
        array = [1, 2, 3, 4, 5]
        
        # Initial stats
        self.assertEqual(searcher.get_hit_ratio(), 0.0)
        
        # One miss
        searcher.search(array, 1)
        self.assertEqual(searcher.get_hit_ratio(), 0.0)
        
        # One hit
        searcher.search(array, 2)
        self.assertEqual(searcher.get_hit_ratio(), 0.5)
        
        # Another hit
        searcher.search(array, 3)
        self.assertAlmostEqual(searcher.get_hit_ratio(), 0.667, places=2)


class TestDataSearchLibrary(unittest.TestCase):
    """Test the DataSearchLibrary class"""
    
    def test_auto_method_selection(self):
        """Test automatic method selection based on array size"""
        lib = DataSearchLibrary(hash_threshold=5)
        
        # Small array should use linear search
        small_array = [1, 2, 3, 4]
        result = lib.find_in_array(small_array, 3)
        self.assertEqual(result, 2)
        
        # Large array should use hash search
        large_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = lib.find_in_array(large_array, 7)
        self.assertEqual(result, 6)
    
    def test_forced_methods(self):
        """Test forcing specific search methods"""
        lib = DataSearchLibrary()
        array = [10, 20, 30, 40, 50]
        
        # Force linear search
        result = lib.find_in_array(array, 30, method='linear')
        self.assertEqual(result, 2)
        
        # Force hash search
        result = lib.find_in_array(array, 40, method='hash')
        self.assertEqual(result, 3)
    
    def test_batch_search(self):
        """Test batch search functionality"""
        lib = DataSearchLibrary()
        array = [10, 20, 30, 40, 50]
        items = [20, 40, 60, 30]  # 60 doesn't exist
        
        results = lib.batch_search(array, items)
        expected = {20: 1, 40: 3, 60: None, 30: 2}
        self.assertEqual(results, expected)
    
    def test_edge_cases(self):
        """Test edge cases for library"""
        lib = DataSearchLibrary()
        
        # Empty array
        self.assertIsNone(lib.find_in_array([], 1))
        
        # None array
        self.assertIsNone(lib.find_in_array(None, 1))
        
        # Empty batch search
        results = lib.batch_search([1, 2, 3], [])
        self.assertEqual(results, {})
    
    def test_cache_management(self):
        """Test cache management methods"""
        lib = DataSearchLibrary(enable_stats=True)
        array = [1, 2, 3, 4, 5, 6]  # Above default threshold
        
        # Use hash search to populate cache
        lib.find_in_array(array, 3, method='hash')
        
        stats = lib.get_stats()
        self.assertIn('hash_threshold', stats)
        self.assertIn('hash_searcher_stats', stats)
        
        # Clear caches
        lib.clear_caches()
        # After clearing, the array should not be cached
        self.assertFalse(lib.hash_searcher.contains_array(array))


class TestCacheDecorator(unittest.TestCase):
    """Test the cache_with_ttl decorator"""
    
    def test_basic_caching(self):
        """Test basic decorator functionality"""
        call_count = 0
        
        @cache_with_ttl(ttl=60)
        def test_function(x, y=10):
            nonlocal call_count
            call_count += 1
            return x + y
        
        # First call - function should be executed
        result1 = test_function(5, y=15)
        self.assertEqual(result1, 20)
        self.assertEqual(call_count, 1)
        
        # Second call with same args - should use cache
        result2 = test_function(5, y=15)
        self.assertEqual(result2, 20)
        self.assertEqual(call_count, 1)  # Function not called again
        
        # Call with different args - should execute function
        result3 = test_function(10)
        self.assertEqual(result3, 20)
        self.assertEqual(call_count, 2)
    
    def test_ttl_expiration(self):
        """Test TTL expiration in decorator"""
        call_count = 0
        
        @cache_with_ttl(ttl=0.5)  # 0.5 second TTL
        def test_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        # First call
        result1 = test_function(5)
        self.assertEqual(result1, 10)
        self.assertEqual(call_count, 1)
        
        # Immediate second call - cached
        result2 = test_function(5)
        self.assertEqual(result2, 10)
        self.assertEqual(call_count, 1)
        
        # Wait for expiration
        time.sleep(0.6)
        
        # Should execute function again
        result3 = test_function(5)
        self.assertEqual(result3, 10)
        self.assertEqual(call_count, 2)
    
    def test_custom_hash_function(self):
        """Test custom hash function"""
        call_count = 0
        
        def custom_hash(x, y=None):
            return str(x)  # Only consider x for caching
        
        @cache_with_ttl(ttl=60, hash_func=custom_hash)
        def test_function(x, y=10):
            nonlocal call_count
            call_count += 1
            return x + y
        
        # These should be cached as same (x=5)
        result1 = test_function(5, y=10)
        result2 = test_function(5, y=20)  # Different y, but same cache key
        
        self.assertEqual(result1, 15)
        self.assertEqual(result2, 15)  # Should return cached value
        self.assertEqual(call_count, 1)
    
    def test_cache_management_methods(self):
        """Test decorator cache management"""
        @cache_with_ttl(ttl=60)
        def test_function(x):
            return x * 2
        
        # Use the function
        test_function(5)
        
        # Check cache info
        info = test_function.cache_info()
        self.assertEqual(info['cache_size'], 1)
        self.assertEqual(info['ttl'], 60)
        
        # Clear cache
        test_function.clear_cache()
        info = test_function.cache_info()
        self.assertEqual(info['cache_size'], 0)


class TestCacheManager(unittest.TestCase):
    """Test the CacheManager class"""
    
    def setUp(self):
        self.manager = CacheManager()
    
    def test_create_and_get_cache(self):
        """Test cache creation and retrieval"""
        # Create TTL cache
        cache = self.manager.create_cache('test_ttl', 'ttl', maxsize=50, ttl=300)
        self.assertIsNotNone(cache)
        
        # Get the same cache
        retrieved_cache = self.manager.get_cache('test_ttl')
        self.assertIs(cache, retrieved_cache)
        
        # Create LRU cache
        lru_cache = self.manager.create_cache('test_lru', 'lru', maxsize=100)
        self.assertIsNotNone(lru_cache)
        
        # Test cache list
        caches = self.manager.list_caches()
        self.assertIn('test_ttl', caches)
        self.assertIn('test_lru', caches)
    
    def test_duplicate_cache_name(self):
        """Test handling of duplicate cache names"""
        self.manager.create_cache('test', 'ttl')
        
        with self.assertRaises(ValueError):
            self.manager.create_cache('test', 'lru')
    
    def test_invalid_cache_type(self):
        """Test invalid cache type handling"""
        with self.assertRaises(ValueError):
            self.manager.create_cache('test', 'invalid_type')
    
    def test_nonexistent_cache(self):
        """Test accessing non-existent cache"""
        with self.assertRaises(KeyError):
            self.manager.get_cache('nonexistent')
    
    def test_cache_operations(self):
        """Test cache operations through manager"""
        cache = self.manager.create_cache('test', 'ttl', maxsize=10, ttl=60)
        
        # Use the cache
        cache['key1'] = 'value1'
        cache['key2'] = 'value2'
        
        # Get cache info
        info = self.manager.get_cache_info('test')
        self.assertEqual(info['name'], 'test')
        self.assertEqual(info['type'], 'ttl')
        self.assertEqual(info['size'], 2)
        self.assertEqual(info['maxsize'], 10)
        self.assertEqual(info['ttl'], 60)
        
        # Clear specific cache
        self.manager.clear_cache('test')
        self.assertEqual(len(cache), 0)
    
    def test_clear_all_caches(self):
        """Test clearing all caches"""
        cache1 = self.manager.create_cache('cache1', 'ttl')
        cache2 = self.manager.create_cache('cache2', 'lru')
        
        cache1['key1'] = 'value1'
        cache2['key2'] = 'value2'
        
        self.assertEqual(len(cache1), 1)
        self.assertEqual(len(cache2), 1)
        
        self.manager.clear_all_caches()
        
        self.assertEqual(len(cache1), 0)
        self.assertEqual(len(cache2), 0)
    
    def test_get_all_cache_info(self):
        """Test getting info for all caches"""
        self.manager.create_cache('cache1', 'ttl', ttl=300)
        self.manager.create_cache('cache2', 'lru', maxsize=50)
        
        all_info = self.manager.get_cache_info()
        
        self.assertIn('cache1', all_info)
        self.assertIn('cache2', all_info)
        self.assertEqual(all_info['cache1']['type'], 'ttl')
        self.assertEqual(all_info['cache2']['type'], 'lru')


class TestBenchmarking(unittest.TestCase):
    """Test benchmarking utilities"""
    
    def test_benchmark_basic(self):
        """Test basic benchmarking functionality"""
        # Use small arrays and counts for fast testing
        results = benchmark_search_methods([10, 100], [5, 10])
        
        # Check structure
        self.assertIn('array_size_10', results)
        self.assertIn('array_size_100', results)
        
        size_10_results = results['array_size_10']
        self.assertIn('5_searches', size_10_results)
        self.assertIn('10_searches', size_10_results)
        
        # Check that timing results exist
        search_5_results = size_10_results['5_searches']
        self.assertIn('linear_time', search_5_results)
        self.assertIn('hash_time', search_5_results)
        self.assertIn('auto_time', search_5_results)
        self.assertIn('hash_vs_linear_speedup', search_5_results)
        self.assertIn('hash_cache_stats', search_5_results)
        
        # Verify times are positive numbers
        self.assertGreater(search_5_results['linear_time'], 0)
        self.assertGreater(search_5_results['hash_time'], 0)
        self.assertGreater(search_5_results['auto_time'], 0)
    
    def test_benchmark_default_params(self):
        """Test benchmarking with default parameters"""
        results = benchmark_search_methods([50])
        
        self.assertIn('array_size_50', results)
        size_50_results = results['array_size_50']
        self.assertIn('100_searches', size_50_results)  # Default search count


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple components"""
    
    def test_end_to_end_workflow(self):
        """Test complete workflow with multiple components"""
        # Create cache manager
        manager = CacheManager()
        user_cache = manager.create_cache('user_searches', 'ttl', ttl=300)
        
        # Create search library
        lib = DataSearchLibrary(enable_stats=True)
        
        # Simulate user searches
        arrays = {
            'user1': [1, 2, 3, 4, 5],
            'user2': [10, 20, 30, 40, 50],
            'user3': list(range(100))  # Large array
        }
        
        search_history = {}
        
        for user, array in arrays.items():
            # Search for various items
            searches = [array[0], array[-1], array[len(array)//2]]
            results = lib.batch_search(array, searches)
            
            # Store in user cache
            user_cache[user] = {
                'array_size': len(array),
                'searches': results,
                'timestamp': time.time()
            }
            
            search_history[user] = results
        
        # Verify everything worked
        self.assertEqual(len(search_history), 3)
        self.assertEqual(len(user_cache), 3)
        
        # Check cache manager
        cache_info = manager.get_cache_info('user_searches')
        self.assertEqual(cache_info['size'], 3)
        
        # Check search library stats
        lib_stats = lib.get_stats()
        self.assertIn('hash_searcher_stats', lib_stats)
    
    def test_performance_comparison(self):
        """Test performance comparison between methods"""
        # Create searchers with different cache types
        searchers = {
            'ttl': HashSearcher(cache_type='ttl', enable_stats=True),
            'lru': HashSearcher(cache_type='lru', enable_stats=True),
            'lfu': HashSearcher(cache_type='lfu', enable_stats=True)
        }
        
        array = list(range(1000))
        search_items = [100, 200, 300, 100, 200, 300]  # Repeated items
        
        results = {}
        for cache_type, searcher in searchers.items():
            start_time = time.time()
            
            for item in search_items:
                searcher.search(array, item)
            
            end_time = time.time()
            
            results[cache_type] = {
                'time': end_time - start_time,
                'hit_ratio': searcher.get_hit_ratio(),
                'cache_info': searcher.cache_info()
            }
        
        # All should have found the items
        for cache_type, result in results.items():
            self.assertGreater(result['hit_ratio'], 0)  # Should have some cache hits
            self.assertGreater(result['time'], 0)  # Should have taken some time


def run_performance_demo():
    """Run a performance demonstration"""
    print("\n" + "="*60)
    print("CACHING TOOLS PERFORMANCE DEMONSTRATION")
    print("="*60)
    
    # Demonstrate different cache types
    print("\n1. Cache Type Comparison:")
    print("-" * 30)
    
    cache_types = ['ttl', 'lru', 'lfu']
    array = list(range(1000))
    search_pattern = [100, 200, 300] * 10  # Repeated searches
    
    for cache_type in cache_types:
        searcher = HashSearcher(cache_type=cache_type, enable_stats=True)
        
        start_time = time.time()
        for item in search_pattern:
            searcher.search(array, item)
        elapsed = time.time() - start_time
        
        print(f"{cache_type.upper()} Cache: {elapsed:.4f}s, Hit ratio: {searcher.get_hit_ratio():.2%}")
    
    # Demonstrate library auto-selection
    print("\n2. Library Auto-Selection:")
    print("-" * 30)
    
    lib = DataSearchLibrary(hash_threshold=50, enable_stats=True)
    
    small_arrays = [[1, 2, 3] for _ in range(100)]
    large_arrays = [list(range(100)) for _ in range(10)]
    
    # Test small arrays (should use linear search)
    start_time = time.time()
    for array in small_arrays:
        lib.find_in_array(array, 2)
    small_time = time.time() - start_time
    
    # Test large arrays (should use hash search)
    start_time = time.time()
    for array in large_arrays:
        lib.find_in_array(array, 50)
    large_time = time.time() - start_time
    
    print(f"Small arrays (linear): {small_time:.4f}s")
    print(f"Large arrays (hash): {large_time:.4f}s")
    print(f"Library stats: {lib.get_stats()}")
    
    # Demonstrate decorator
    print("\n3. Decorator Caching:")
    print("-" * 30)
    
    @cache_with_ttl(ttl=60)
    def expensive_operation(n):
        total = 0
        for i in range(n):
            total += i ** 2
        return total
    
    # First call (uncached)
    start_time = time.time()
    result1 = expensive_operation(10000)
    first_time = time.time() - start_time
    
    # Second call (cached)
    start_time = time.time()
    result2 = expensive_operation(10000)
    second_time = time.time() - start_time
    
    print(f"First call (uncached): {first_time:.4f}s")
    print(f"Second call (cached): {second_time:.4f}s")
    print(f"Speedup: {first_time/second_time:.1f}x")
    print(f"Results match: {result1 == result2}")
    
    print("\n" + "="*60)


if __name__ == '__main__':
    # Check if running as test
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # Run unit tests
        unittest.main(argv=[''], exit=False, verbosity=2)
    else:
        # Run both tests and demo
        print("Running unit tests...")
        unittest.main(argv=[''], exit=False, verbosity=1)
        
        # Run performance demo
        run_performance_demo()
        
        print("\nTo run only tests: python caching_tools_test.py test")
        print("To run interactive demo: python caching_tools_test.py")