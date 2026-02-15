def fibonacci_sequence_less_than(n):
    if n <= 0:
        return []
    
    fib_seq = [0, 1]
    while True:
        next_value = fib_seq[-1] + fib_seq[-2]
        if next_value >= n:
            break
        fib_seq.append(next_value)
    
    return fib_seq

# Example usage
N = 50
fib_sequence = fibonacci_sequence_less_than(N)
print(f"Fibonacci sequence less than {N}: {fib_sequence}")