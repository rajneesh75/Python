def add(a, b):
    return a + b


x = 5
assert x > 0, "x should be positive"
assert x == 5, "x should be 10"


assert add(2, 3) == 5, "Test failed: 2 + 3 should be 5"
assert add(-1, 1) == 0, "Test failed: -1 + 1 should be 0"
print("All tests passed!")