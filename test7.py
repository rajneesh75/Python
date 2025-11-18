def add_to(num, target=[]):
    target.append(num)
    return target


list1 = add_to(1)
list2 = add_to(2, [])
list3 = add_to(3)

print(list1, list2, list3)
