tup = {(1, 2, 4): 8, (4, 2, 1): 10, (1, 2): 12}
print(tup)
sum1 = 0
for k in tup:
    sum1 += tup[k]
print(len(tup) + sum1)
