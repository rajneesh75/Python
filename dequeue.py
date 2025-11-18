from collections import deque

# Create a deque
d = deque([1, 2, 3])

# Add to the right end
d.append(4)
print(d)  # Output: deque([1, 2, 3, 4])

# Add to the left end
d.appendleft(0)
print(d)  # Output: deque([0, 1, 2, 3, 4])

# Pop from the right end
d.pop()
print(d)  # Output: deque([0, 1, 2, 3])

# Pop from the left end
d.popleft()
print(d)  # Output: deque([1, 2, 3])
