import itertools

# Infinite counter
for i in itertools.count(5):
    if i > 7: break
    print(i)  # 5, 6, 7

# Cycle through letters
for j, letter in zip(range(7), itertools.cycle(['A', 'B', 'C'])):
    print(letter)  # A, B, C, A, B, C
