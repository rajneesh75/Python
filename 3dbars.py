import numpy as np
import matplotlib.pyplot as plt

# Data for plotting
x = np.array([1, 2, 3, 4, 5])
y = np.array([1, 2, 3, 4, 5])
z = np.zeros_like(x)  # Base of the bars (z=0 for all)

dx = np.ones_like(x)  # Width of bars
dy = np.ones_like(y)  # Depth of bars
dz = np.array([10, 20, 30, 40, 50])  # Height of bars

# Create a figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the 3D bars
ax.bar3d(x, y, z, dx, dy, dz, color='b', zsort='average')

# Add labels
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')

# Set a title
ax.set_title('3D Bar Chart')

# Show the plot
plt.show()
