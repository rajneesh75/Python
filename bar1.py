import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation
from collections import Counter


def update_pheromone(pheromone, ants):
    # Evaporate existing pheromone
    for path in pheromone:
        pheromone[path] = pheromone[path] * (1 - evaporation_rate)

    # Deposits new pheromone for paths that ants have visited
    for i in ants:
        pheromone[i] = pheromone[i] + pheromone_deposit


def update_ants(ants, pheromone):
    # Extract paths and their corresponding pheromone levels
    paths = list(pheromone.keys())
    pheromone_levels = list(pheromone.values())

    # Calculate total pheromone to determine probabilities
    total_pheromone = sum(pheromone_levels)

    probabilities = [level / total_pheromone for level in pheromone_levels]

    # Update each ant's path based on pheromone probabilities
    for i in range(num_ants):
        ants[i] = random.choices(paths, probabilities)[0]


def animate(frame):
    # Update pheromone and ants for the current frame
    update_pheromone(pheromone, ants)
    update_ants(ants, pheromone)

    # Update the bar heights for the second set of bars
    final_count = Counter(ants)
    for i, solution in enumerate(solutions):
        bars2[i].set_height(final_count[solution])
    return bars2


# Parameters
num_ants = 10
num_iterations = 50
evaporation_rate = 0.1
pheromone_deposit = 1.0
paths = 5

# paths space
paths_space = range(paths)

# Initialize ants with random paths
ants = [random.choice(paths_space) for _ in range(num_ants)]

initial_count = Counter(ants)
solutions = sorted(set(initial_count.keys()))

initial_counts = [initial_count[solution] for solution in solutions]

# Initialize pheromone trails for each path
pheromone = {path: 1 for path in paths_space}

fig, ax = plt.subplots()
ax.set_xlabel('Solutions')
ax.set_ylabel('Number of Ants')
plt.ion()
bar_width = 0.35

# Initial bars (blue)
bars1 = ax.bar(solutions - bar_width / 2, initial_counts, bar_width, color='blue', label='Initial')
ax.set_xticks(solutions)

# Animated bars (orange)
bars2 = ax.bar(solutions + bar_width / 2, initial_counts, bar_width, color='orange', label='Final')

ax.legend()
plt.tight_layout()

# Create animation
ani = animation.FuncAnimation(fig, animate, frames=num_iterations, interval=500, blit=True)

# Display the animation
plt.show()

# Final paths
print(f"\nFinal ants {ants}")
print(f"Final counts {Counter(ants)}")
