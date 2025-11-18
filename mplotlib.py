import matplotlib.pyplot as plt
import numpy as np

# Data
x = np.linspace(0, 10, 1000)
y = np.sin(x)

# Plot
plt.plot(x, y)
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('Smooth Sine Wave')
plt.grid(True)
plt.show()