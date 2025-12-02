

def example_function():
    total = 0
    for i in range(10000):
        for j in range(100):
            total += (i * j) % 7
    return total

print(example_function())