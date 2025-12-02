
def read_data():
    with open("customers-100.csv") as f:
        for line in f:
            yield line

g = read_data()
print(next(g))  # → 0
print(next(g))  # → 0