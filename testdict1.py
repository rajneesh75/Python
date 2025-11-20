d = dict()
print (enumerate(range(2)))
for x in enumerate(range(2)):
    d[x[0]] = x[1]
    d[x[1]+7] = x[0]
print(d)