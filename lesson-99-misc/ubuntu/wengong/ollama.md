>>> write a python script to calculate fibonacci sequence less than N
Certainly! Below is a Python script that calculates the Fibonacci sequence up to but not including a given 
number \( N \):

```python
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
```

### Explanation:
- The function `fibonacci_sequence_less_than(n)` takes an integer \( n \) as input.
- It initializes a list `fib_seq` with the first two Fibonacci numbers, 0 and 1.
- A while loop is used to generate subsequent Fibonacci numbers. If the next number in the sequence is 
greater than or equal to \( n \), the loop breaks.
- Finally, the function returns the generated Fibonacci sequence.

### Example Output:
For \( N = 50 \), the output will be:
```
Fibonacci sequence less than 50: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
