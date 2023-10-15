#!/usr/bin/env python3
# countasync.py

import asyncio

async def count(i: int, sl_time: float = 1.0):
    print(f"Enter: {i}")
    await asyncio.sleep(sl_time)
    print(f"Exit: {i}")

async def main():
    await asyncio.gather(count(1, 1.4), count(2, 2.1), count(3, 0.9))

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")