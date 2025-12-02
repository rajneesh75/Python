def gen():
    for i in range(4):
        yield i


g = gen()
print(next(g))  # → 0
print(next(g))
print(next(g))
print(list(g))  # ?
