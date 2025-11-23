numbers = [1, 2, 3, 4, 5]
for i, num in enumerate(numbers):
    print(i % 2)
    if i % 2 == 0:

        continue
    print(num, end=' ')
