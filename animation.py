import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Sample categories
categories = ['A', 'B', 'C', 'D']


# Function to update the bar chart for each frame with dynamically generated data
def update(frame, bar_objects):
    # Generate dynamic data (for example, random values or data from a live source)
    new_values = [np.random.randint(0, 10) for _ in categories]
    for bar, new_height in zip(bar_objects, new_values):
        bar.set_height(new_height)
    return bar_objects


# Set up the figure and axis
fig, ax = plt.subplots()
initial_values = [0] * len(categories)  # Initial values, all set to zero
bars = ax.bar(categories, initial_values)

# Set up plot limits (adjust if needed)
ax.set_ylim(0, 10)

# Create animation with dynamically generated data
ani = animation.FuncAnimation(fig, update, frames=100, fargs=(bars,), blit=False)

# Display the animation
plt.show()
