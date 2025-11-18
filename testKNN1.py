import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

np.random.seed(42)

# Generate 20 data points with 2 dimensions
X = np.random.rand(20, 2)
print(X)

# Display Embeddings
n = range(len(X))
k = 4

neigh = NearestNeighbors(n_neighbors=k, algorithm='brute', metric='euclidean')
neigh.fit(X)

# Display Query with data
n = range(len(X))
neighbours = neigh.kneighbors([[0.6, 0.6]], k, return_distance=True)
print(neighbours)

fig, ax = plt.subplots()
ax.scatter(X[:, 0], X[:, 1])
ax.scatter(0.6, 0.6, c='red', label='Query')
ax.legend()
for i, txt in enumerate(n):
    ax.annotate(txt, (X[i, 0], X[i, 1]))

plt.show()
