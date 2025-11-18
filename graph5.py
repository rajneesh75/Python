import networkx as nx
import matplotlib.pyplot as plt

DG = nx.DiGraph()
DG.add_edges_from([("A", "B"), ("B", "C"), ("C", "A")])
nx.draw(DG, with_labels=True, node_color='lightgreen')
plt.show()