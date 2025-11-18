import matplotlib.pyplot as plt

# Data for plotting
x = [1, 2, 3, 4, 5]  # X-axis values
y = [2, 4, 1, 8, 7]  # Y-axis values

# Create a figure and axis
plt.figure(figsize=(8, 5))

# Plot the data
plt.plot(x, y, color='blue', marker='o', linestyle='--', linewidth=2, markersize=8, label='Line 1')

# Add title and labels
plt.title('Sample Line Chart', fontsize=16)
plt.xlabel('X-axis', fontsize=12)
plt.ylabel('Y-axis', fontsize=12)

# Add grid
plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

# Add legend
plt.legend(loc='upper left')

# Show the plot
plt.show()
