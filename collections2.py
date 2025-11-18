from collections import deque

d = deque([1, 2, 3])
d.append(4)      # add to right
print(d)

d.appendleft(0)  # add to left
print(d)

d.pop()          # remove from right
print(d)

d.popleft()      # remove from left
print(d)