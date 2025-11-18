import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# Data
x = np.linspace(0, 10, 1000)
y = np.sin(x)

# Plot
sns.set(style="whitegrid")
sns.lineplot(x=x, y=y)
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('Smooth Sine Wave with Seaborn')
plt.show()