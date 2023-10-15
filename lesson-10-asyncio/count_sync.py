#!/usr/bin/env python3
# countasync.py

import time

def count(i: int, sl_time: float = 1.0):
    print(f"Enter: {i}")
    time.sleep(sl_time)
    print(f"Exit: {i}")

def main():
    count(1, 1.4)
    count(2, 2.1)
    count(3, 0.9)

if __name__ == "__main__":

    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")