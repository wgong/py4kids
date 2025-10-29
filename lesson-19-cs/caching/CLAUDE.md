# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a learning-focused Python project that demonstrates caching techniques and algorithms. It's part of the py4kids lesson series, specifically lesson 19 covering computer science concepts related to caching.

## Core Architecture

### Main Components

1. **caching_tools.py** - Production-ready caching library with multiple cache types
   - `TTLCacheSimple`: Basic time-to-live cache implementation
   - `HashSearcher`: Cached hash-based array search with multiple cache strategies (TTL, LRU, LFU, TLRU)
   - `DataSearchLibrary`: High-level library with automatic method selection
   - `CacheManager`: Multi-cache management system
   - `cache_with_ttl`: Function decorator for caching

2. **caching_tool_blog.ipynb** - Interactive Jupyter notebook for learning and exploration
   - Demonstrates all caching concepts with live examples
   - Performance comparisons between cache types
   - Educational content with markdown explanations

3. **caching_tools_test.py** - Comprehensive test suite
   - Unit tests for all components
   - Performance benchmarking utilities
   - Integration tests
   - Demo functions for interactive testing

4. **Legacy files** (for reference):
   - `ttl_cache.py`: Original TTL cache implementation with API examples
   - `test_ttl_cache.py`: Basic TTL cache testing
   - `caching_tool_blog.md`: Original blog post (converted to notebook)

## Common Development Tasks

### Running Tests
```bash
# Run all tests with detailed output
python caching_tools_test.py

# Run only unit tests
python caching_tools_test.py test

# Run with pytest if available
python -m pytest caching_tools_test.py -v
```

### Using the Library
```python
# Import the main components
from caching_tools import HashSearcher, DataSearchLibrary, cache_with_ttl

# Basic usage examples in the files themselves
python caching_tools.py  # Runs demo
```

### Working with the Notebook
```bash
# Start Jupyter notebook
jupyter notebook caching_tool_blog.ipynb
```

## Dependencies

Required packages (install with `pip install`):
- `cachetools` - Advanced caching implementations
- `requests` - For API examples (optional)
- `beautifulsoup4` - For web scraping examples (optional) 
- `jupyter` - For notebook (optional)

The code is designed to gracefully handle missing optional dependencies.

## Learning Workflow Integration

This repository demonstrates an effective learning workflow combining Claude web chat with Claude Code:

1. **Research Phase** (Claude web chat): Generate comprehensive blog content with theory and examples
2. **Interactive Learning** (Jupyter notebook): Convert blog to interactive format for hands-on exploration
3. **Production Code** (Python modules): Extract reusable components into clean, documented libraries
4. **Quality Assurance** (Test suites): Comprehensive testing with performance benchmarks
5. **Documentation** (This file): Central guidance for future development

## Key Design Patterns

- **Thread-safe operations**: All caches use threading.RLock() for concurrent access
- **Graceful degradation**: Fallback mechanisms for unhashable types and missing dependencies
- **Configurable strategies**: Multiple cache types (TTL, LRU, LFU, TLRU) with same interface
- **Statistics tracking**: Optional performance monitoring and hit/miss ratios
- **Educational focus**: Clear examples and comprehensive documentation

## Testing Strategy

- **Unit tests**: Individual component testing
- **Integration tests**: End-to-end workflow testing  
- **Performance benchmarks**: Timing comparisons between different approaches
- **Thread safety tests**: Concurrent access validation
- **Edge case testing**: Empty arrays, None values, unhashable elements

## Performance Considerations

- Arrays > 100 elements automatically use hash search for O(1) lookups
- Cache key generation optimized: tries built-in hash() first, falls back to pickle+md5
- Thread-safe but locks are held for minimal time
- TTL cleanup happens automatically on access
- Memory bounds enforced through maxsize parameters

This codebase serves as both a learning resource and a production-ready caching library, making it ideal for educational projects that can evolve into real applications.