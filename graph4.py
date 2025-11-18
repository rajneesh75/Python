import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_edge('A', 'B')
G.add_edge('A', 'C')
G.add_edge('B', 'D')
G.add_edge('B', 'E')
G.add_edge('B', 'F')
G.add_edge('F', 'C')
G.add_edge('C', 'E')
G.add_edge('D', 'F')
G.add_edge('C', 'F')

# for u, v, data in G.edges(data=True):
#    print(u, v, data['weight'])
path = nx.shortest_path(G, source='A', target='F')
print("Shortest path from A to F:", path)
print(dict(G.degree()))
print(nx.find_cycle(G))

nx.draw(G, with_labels=True, node_color='lightblue', node_size=1500, font_size=12, edge_color='gray', width=2,
        style='dashed')
plt.show()
