import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def create_positions(num_nodes):
    """Generate positions for nodes in a hexagon shape."""
    positions = {}
    for i in range(num_nodes):
        angle = 2 * np.pi * i / num_nodes
        x = np.cos(angle)
        y = np.sin(angle)
        positions[i] = (x, y)
    return positions


def create_edges(num_nodes):
    """Generate edges to form a hexagon."""
    edges = [(i, (i + 1) % num_nodes) for i in range(num_nodes)]
    return edges


def get_diamond_coords(center, count):
    """Generate coordinates for the diamond shape around the center node."""
    angle_offset = 2 * np.pi / count
    radius = 0.1  # Adjust this radius as needed for visual spacing
    return [(center[0] + radius * np.cos(angle_offset * i),
             center[1] + radius * np.sin(angle_offset * i)) for i in range(count)]


def update_magnet_position(positions, node_person_counts):
    """Calculate the new position for the magnet based on where the people are swarming the most."""
    max_person_node = max(node_person_counts, key=node_person_counts.get)
    high_weight_factor = 5  # Factor to move closer to the high weight node
    total_weight = sum(node_person_counts.values()) + (high_weight_factor - 1) * node_person_counts[max_person_node]
    new_magnet_x = (sum(positions[node][0] * node_person_counts[node] for node in node_person_counts) +
                    (high_weight_factor - 1) * positions[max_person_node][0] * node_person_counts[
                        max_person_node]) / total_weight
    new_magnet_y = (sum(positions[node][1] * node_person_counts[node] for node in node_person_counts) +
                    (high_weight_factor - 1) * positions[max_person_node][1] * node_person_counts[
                        max_person_node]) / total_weight
    return new_magnet_x, new_magnet_y


def draw_graph(num_nodes, selections):
    """Draw the graph with nodes, edges, and swarming people."""
    positions = create_positions(num_nodes)
    edges = create_edges(num_nodes)
    g = nx.Graph()
    g.add_edges_from(edges)

    # Calculate the number of people swarming at each node
    node_person_counts = {node: 0 for node in range(num_nodes)}
    node_person_map = {node: [] for node in range(num_nodes)}
    for person, node in selections.items():
        node_person_counts[node] += 1
        node_person_map[node].append(person)

    # Calculate new magnet position
    magnet_x, magnet_y = update_magnet_position(positions, node_person_counts)
    positions['magnet'] = (magnet_x, magnet_y)

    # Draw the graph
    plt.figure(figsize=(10, 10))
    nx.draw(g, pos=positions, with_labels=False, node_size=700, node_color='skyblue', edge_color='gray', font_size=10)

    # Add labels to the nodes
    labels = {i: f'Node {i}' for i in range(num_nodes)}
    labels['magnet'] = ''
    nx.draw_networkx_labels(g, pos=positions, labels=labels, font_size=12, font_color='green')

    # Draw the central magnet as a larger node
    nx.draw_networkx_nodes(g, pos=positions, nodelist=['magnet'], node_size=1000, node_color='yellow')

    # Draw circles for each person's selection inside a diamond shape around the selected nodes
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'magenta']
    for node, count in node_person_counts.items():
        if count > 0:
            diamond_coords = get_diamond_coords(positions[node], count)
            for j, (person, coord) in enumerate(zip(node_person_map[node], diamond_coords)):
                plt.plot(*coord, 'o', color=colors[j % len(colors)], markersize=10, alpha=0.6, label=f'{person}')
                plt.text(coord[0], coord[1], person, fontsize=10, ha='center', va='center', color='white',
                         bbox=dict(facecolor='black', alpha=0.7, edgecolor='black', boxstyle='round,pad=0.3'))

    # Manually add legend entries
    for i, color in enumerate(colors[:len(selections)]):
        plt.plot([], [], 'o', color=color, markersize=10, alpha=0.6, label=f'Person {i + 1}')

    plt.legend(loc='upper right')

    # Draw the circular connections
    # circle = plt.Circle((0, 0), 1.2, color='blue', fill=False, linestyle='dotted')
    # plt.gca().add_patch(circle)

    # Show plot
    plt.title("Swarm AI Graph with Magnet and Person Selections")
    plt.axis('off')
    plt.show()


# Example usage:
num_nodes = 10  # Total number of nodes in the hexagon
selections = {
    1: 3,  # Person 1 chooses 3rd node
    2: 1,  # Person 2 chooses 1st node
    3: 2,  # Person 3 chooses 2nd node
    4: 3,  # Person 4 chooses 3rd node
    5: 4,  # Person 5 chooses 4th node
    6: 5,  # Person 6 chooses 6th node
    7: 3  # Person 7 chooses 3rd node
}

draw_graph(num_nodes, selections)
