import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_weighted_edges_from([
    ('A', 'B', 4),
    ('A', 'C', 2),
    ('B', 'C', 1),
    ('B', 'D', 5),
    ('C', 'D', 8)
])

nx.draw(G, with_labels=True, node_color='lightblue', node_size=1500, font_size=12, edge_color='gray', width=2,
        style='solid')


print(nx.shortest_path(G, 'A', 'D', weight='weight'))
print(nx.shortest_path_length(G, 'A', 'D', weight='weight'))
plt.show()