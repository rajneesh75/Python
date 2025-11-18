import tsplib95
import numpy as np

filename = 'att48.tsp'
with open(filename) as f:
    text = f.read()
problem = tsplib95.parse(text)
nodes = list(problem.get_nodes())
distances = np.zeros((len(nodes), len(nodes)))

for i in range(len(nodes)):
    for j in range(len(nodes)):
        if i != j:
            distances[i][j] = problem.get_weight(i + 1, j + 1)

print("Loaded TSP dataset with {} nodes.".format(len(nodes)))
