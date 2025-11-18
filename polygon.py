import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Define the vertices of the polygon
vertices = [(1, 2), (3, 4), (5, 2), (4, 0), (2, 0)]

# Create a figure and axis
fig, ax = plt.subplots()

# Create a polygon patch
polygon = Polygon(vertices, closed=True, fill=False, edgecolor='black', facecolor='blue')

# Add the polygon to the plot
ax.add_patch(polygon)

# Set the limits of the plot
ax.set_xlim(0, 6)
ax.set_ylim(-1, 5)

# Display the plot
plt.grid(True)
plt.show()
