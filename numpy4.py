import numpy as np

mat = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(mat[1, 2])  # 6
print(mat[:, 1])  # column 1
print(mat[1:, :2])
