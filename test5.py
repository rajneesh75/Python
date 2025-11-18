def squares(n):
    for i in range(n):
        yield i * i   # yield gives one value at a time


gen = squares(5)
print(next(gen))
print(next(gen))
