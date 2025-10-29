import time
import functools
from typing import Any, Callable, Dict, Tuple, Optional
import hashlib
import pickle

class TTLCache:
    """Time-To-Live cache implementation"""
    
    def __init__(self):
        self._cache: Dict[str, Tuple[Any, float]] = {}
    
    def get(self, key: str, ttl: float) -> Tuple[bool, Any]:
        """Get item from cache if not expired"""
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
        self._cache[key] = (value, time.time())
    
    def clear(self) -> None:
        """Clear all cached items"""
        self._cache.clear()
    
    def size(self) -> int:
        """Get number of cached items"""
        return len(self._cache)

# Global cache instance
_global_cache = TTLCache()

def cache(ttl: float = 3600, hash_func: Optional[Callable] = None):
    """
    Decorator to cache function results with TTL (Time-To-Live)
    
    Args:
        ttl: Time-to-live in seconds (default: 3600 = 1 hour)
        hash_func: Optional custom hash function for cache keys
    
    Usage:
        @cache(ttl=3600)  # Cache for 1 hour
        def download_data(url):
            # Your function implementation
            pass
    """
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
                print(f"Cache HIT for {func.__name__}")
                return cached_value
            
            # Cache miss - call function and store result
            print(f"Cache MISS for {func.__name__}")
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

# Example usage:
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

# @cache(ttl=10)  # Cache for 60 seconds
def download_data(url: str = "http://worldtimeapi.org/api/timezone/Etc/UTC") -> dict:
    """
    Fetch current time from a reliable time API
    
    This function demonstrates TTL caching by fetching the current time.
    The key insight: each call gets the EXACT time when the API was called,
    so you can see if results are cached (same time) or fresh (different time).
    """
    print(f"Fetching current time from {url}...")
    
    try:
        # Use a reliable time API instead of web scraping
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        if 'worldtimeapi.org' in url:
            # WorldTimeAPI returns JSON
            data = response.json()
            api_time = data['datetime']
            # Parse the ISO datetime and format it nicely
            api_datetime = datetime.fromisoformat(api_time.replace('Z', '+00:00'))
            current_time = api_datetime.strftime('%H:%M:%S')
            location = data.get('timezone', 'UTC')
        else:
            # Fallback for other APIs
            current_time = datetime.now().strftime('%H:%M:%S')
            location = 'Unknown'
        
        # IMPORTANT: Record the local time when we made this call
        local_call_time = datetime.now().strftime('%H:%M:%S')
        
        return {
            'api_time': current_time,           # Time from the API
            'local_call_time': local_call_time, # Local time when API was called
            'location': location,
            'fetched_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source_url': url
        }
        
    except Exception as e:
        print(f"Error fetching time from API: {e}")
        # Always fallback to local time with current timestamp
        local_time = datetime.now().strftime('%H:%M:%S')
        return {
            'api_time': 'API_ERROR',
            'local_call_time': local_time,      # This shows when the call was actually made
            'location': 'Local System (API failed)',
            'fetched_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source_url': 'local_fallback',
            'error': str(e)
        }

@cache(ttl=1800)  # Cache for 30 minutes
def get_market_data(symbol: str, date: str = None) -> dict:
    """Get market data with optional date parameter"""
    print(f"Fetching market data for {symbol} on {date}...")
    time.sleep(0.5)
    return {
        'symbol': symbol,
        'open': 145.00,
        'high': 152.00,
        'low': 144.50,
        'close': 150.00,
        'date': date or time.strftime('%Y-%m-%d')
    }

# Advanced: Custom hash function example
def url_hash(*args, **kwargs):
    """Custom hash function that only considers the URL parameter"""
    url = args[0] if args else kwargs.get('url', '')
    return hashlib.md5(url.encode()).hexdigest()

@cache(ttl=7200, hash_func=url_hash)  # Cache for 2 hours with custom hash
def download_data_advanced(url: str, retries: int = 3) -> dict:
    """Advanced version that ignores 'retries' parameter in caching"""
    print(f"Downloading from {url} (retries={retries})")
    return {'data': 'sample', 'url': url}

if __name__ == "__main__":
    print("=== Testing TTL Cache with Time API ===")
    print("Note: You'll need: pip install requests")
    print()
    
    try:
        # Test 1: First call - cache miss
        print("1. First call (cache miss - should see API fetch):")
        result1 = download_data()
        print(f"   API Time: {result1['api_time']}")
        print(f"   Local Call Time: {result1['local_call_time']}")
        print(f"   Fetched at: {result1['fetched_at']}")
        print()
        
        # Test 2: Immediate second call - cache hit
        print("2. Immediate second call (cache hit - no API fetch):")
        result2 = download_data()
        print(f"   API Time: {result2['api_time']}")
        print(f"   Local Call Time: {result2['local_call_time']}")
        print(f"   Fetched at: {result2['fetched_at']}")
        print(f"   Same result? {result1['fetched_at'] == result2['fetched_at']}")
        print()
        
        # Test 3: Show time progression
        print("3. Wait 3 seconds and call again (still cached):")
        time.sleep(3)
        result3 = download_data()
        print(f"   Local Call Time: {result3['local_call_time']}")
        print(f"   Still cached? {result1['fetched_at'] == result3['fetched_at']}")
        print()
        
        print("4. Cache information:")
        print(f"   {download_data.cache_info()}")
        print()
        
        print("=== Key Points for Testing TTL ===")
        print("• 'local_call_time' shows WHEN the function was originally called")
        print("• If cached: same 'local_call_time' and 'fetched_at' timestamp")
        print("• If fresh: new 'local_call_time' and 'fetched_at' timestamp")
        print("• Wait 60+ seconds to see cache expiration")
        print("• The 'Cache HIT/MISS' messages show caching behavior")
        
    except ImportError:
        print("Please install: pip install requests")
    except Exception as e:
        print(f"Error during testing: {e}")
        print("The function will fallback to local time if API fails.")