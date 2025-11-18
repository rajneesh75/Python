import numpy as np

a = np.array([1, 2, 3])
b = np.array([[1, 2, 3], [4, 5, 6]])

print(a)        # [1 2 3]
print(b)


print(a.ndim)   # 1  (dimensions)
print(b.shape)  # (2, 3)
print(b.size)   # 6  (total elements)
print(b.dtype)  # int64 (data type)