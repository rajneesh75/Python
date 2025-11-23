numbers = [3, 7, 2, 8, 5]
print(list(enumerate(numbers)))
for i, num in enumerate(numbers):
    if i == num:
        break
    print(num, end=' ')