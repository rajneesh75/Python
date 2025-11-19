a = [1, 2, 3, 4]
b = a
c = a.copy()
d = a
a[0] = [5]
print(a, b, c, d) 