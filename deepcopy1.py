import copy

list1 = [[1, 2], [3, 4]]

shallow = copy.copy(list1)
deep = copy.deepcopy(list1)

list1[0][0] = 99

print("Original:", list1)
print("Shallow Copy:", shallow)
print("Deep Copy:", deep)