from collections import Counter

c = Counter(['a', 'b', 'a', 'c', 'b', 'a'])
print(c)

print(c.most_common(1))
print(c.total())
