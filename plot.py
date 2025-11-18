import matplotlib.pyplot as plt

def plot_tsp(path, points):
    x = [points[point + 1][0] for point, _ in path]
    y = [points[point + 1][1] for point, _ in path]
    x.append(x[0])
    y.append(y[0])

    plt.plot(x, y, 'o-', color='blue')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('TSP Solution using ACO')
    plt.show()

coordinates = problem.node_coords
plot_tsp(shortest_path[0], coordinates)
