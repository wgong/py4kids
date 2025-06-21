# Comparative Studies and Benchmarks

Asked Gemini for how to improve RAG app performance in this [chat](https://gemini.google.com/app/1223681882e88c01)

see answer-by-gemini.md

## Key Benchmark Metrics

- Requests Per Second (RPS) / Throughput: How many requests can the server handle in a given time period. This is often the primary metric for "speed."
- Latency: The time it takes for a request to be processed and a response returned. This can be average, median, or percentile (e.g., P99 latency, which is the latency for 99% of requests).
- CPU/Memory Utilization: How efficiently the framework uses system resources.
- Concurrency: How well the framework handles multiple simultaneous requests.
    - Workload Type:
    - CPU-bound: Operations that heavily rely on CPU computation (e.g., complex calculations, image processing, local ML inference).
    - I/O-bound: Operations that involve waiting for external resources (e.g., database queries, API calls to other services like Claude, file I/O). RAG applications are often highly I/O-bound.
    - Simple Endpoints: Basic "hello world" or JSON responses, which primarily test framework overhead.


## Blogs 

- detailed code-level comparison : https://betterstack.com/community/guides/scaling-python/flask-vs-fastapi/
- fair comparison: https://www.turing.com/kb/fastapi-vs-flask-a-detailed-comparison
- bare minimal : https://medium.com/@krishtech/performance-showdown-fastapi-vs-flask-in-high-traffic-applications-1cb041d2ae51

# Web Framework Benchmarks
https://www.techempower.com/benchmarks/#section=data-r23


## Case Study 1

- [src](https://github.com/agusmakmun/flask-django-quart-fastapi-performance-test-comparison)
    - fork: ~/projects/wgong/flask-django-quart-fastapi-performance-test-comparison

## Case Study 2
compare various ASGI servers, with details on FastAPI

- [src](https://github.com/klen/py-frameworks-bench)
    - [fastapi](https://github.com/klen/py-frameworks-bench/blob/develop/frameworks/fastapi/app.py)


## Case Study 3

basic compare Flask vs FastAPI
- has helper functions
- [src](https://github.com/steveryb/fastapi-flask-benchmark/tree/master)


# Code Example

## Note Taking App

Create APIs for SQLite db CRUD operations
- digital-duck/notes/deploy/backend/main.py

## LangChain