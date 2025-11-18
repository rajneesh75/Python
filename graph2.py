import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_edges_from([("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")])

nx.draw(G, with_labels=True, node_color='lightblue', node_size=1500, font_size=12)
plt.show()