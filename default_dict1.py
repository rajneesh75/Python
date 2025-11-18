from collections import defaultdict

dd = defaultdict(int)
dd['a'] += 1
dd['b'] += 2
print(dd['a'])
print(dd['b'])
print(dd['c'])  # returns 0, not KeyError