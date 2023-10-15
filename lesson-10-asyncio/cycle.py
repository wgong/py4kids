from itertools import cycle
def endless():
    """Yields 9, 8, 7, 6, 9, 8, 7, 6, forever"""
    yield from cycle((9, 8, 7, 6))

n_max = 21

n = 0
e = endless()
total = 0
for i in e:
    if total < 30:
        print(f"{i} ({n}) > ", end=" ")
        total += i
    else:
        total = 0
        print(f"{i} ({n}) > ", end=" ")
        total += i

    if n > n_max:
        print("Breaking...")
        # Pause execution. We can resume later.
        break
        
    n += 1
