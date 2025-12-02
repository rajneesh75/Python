from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    """Return the nth Fibonacci number using memoization."""
    if n < 0:
        raise ValueError("Input should be a non-negative integer.")
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

