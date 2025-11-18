x = [1, 2, 3, 4]

total_sum = 0.0
for i in range(len(x) // 4):
    print(i)

    time = x[i * 4]
    print(time)

    cost = 1 / (time ** 2)
    print(cost)

    efforts = x[i * 4 + 2]
    print(efforts)

    effectiveness = x[i * 4 + 3]
    print(effectiveness)

    total_sum += time + cost + efforts + effectiveness
    print(total_sum)
