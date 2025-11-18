import random
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np


def plot_ant_distribution(initial_ants, final_ants, title):
    initial_count = Counter(initial_ants)
    final_count = Counter(final_ants)

    solutions = sorted(set(initial_count.keys()).union(final_count.keys()))
    initial_counts = [initial_count[solution] for solution in solutions]
    final_counts = [final_count[solution] for solution in solutions]

    bar_width = 0.35
    index = np.arange(len(solutions))

    plt.bar(index, initial_counts, bar_width, color='b', label='Initial')
    plt.bar(index + bar_width, final_counts, bar_width, color='r', label='Final')

    plt.xlabel('Solutions')
    plt.ylabel('Number of Ants')
    plt.title(title)
    plt.xticks(index + bar_width / 2, solutions)
    plt.legend()
    plt.show()


def update_pheromone(pheromone, ants):
    print("\nupdate_pheromone")

    # Evaporate existing pheromone
    for path in pheromone:
        pheromone[path] = pheromone[path] * (1 - evaporation_rate)
    print(f"pheromone after evaporation {type(pheromone)} {pheromone}")

    # Deposits new pheromone for paths that ants have visited
    for i in ants:
        pheromone[i] = pheromone[i] + pheromone_deposit
    print(f"pheromone after deposit {type(pheromone)} {pheromone}")


def update_ants(ants, pheromone):
    print("\nupdate_ants")

    # Extract paths and their corresponding pheromone levels
    paths = list(pheromone.keys())
    pheromone_levels = list(pheromone.values())

    # Calculate total pheromone to determine probabilities
    total_pheromone = sum(pheromone_levels)
    print(f"total_pheromone: {total_pheromone}")

    probabilities = []
    for level in pheromone_levels:
        probabilities.append(level / total_pheromone)
    print(f"probabilities: {probabilities}")

    # Update each ant's path based on pheromone probabilities
    for i in range(num_ants):
        ants[i] = random.choices(paths, probabilities)[0]
    print(f"Updated ants {type(ants)} {ants}")


# Parameters
num_ants = 10
num_iterations = 3
evaporation_rate = 0.1
pheromone_deposit = 1.0
paths = 5

# paths space
paths_space = range(paths)

# Initialize ants with random paths
ants = []
for _ in range(num_ants):
    ants.append(random.choice(paths_space))

# ants = [0, 0, 0, 2, 0, 0, 2, 0, 0, 0]
initial_ants = ants.copy()
print(f"Initial ants {type(ants)} {ants}")


# Initialize pheromone trails for each ant
pheromone = {}
for path in paths_space:
    pheromone[path] = 1

print(f"pheromone {type(pheromone)} {pheromone}")

for iteration in range(num_iterations):
    update_pheromone(pheromone, ants)
    update_ants(ants, pheromone)

# Final paths
print(f"\nInitial ants {initial_ants}")
print(f"Initial counts {Counter(initial_ants)}")
print(f"\nFinal ants {ants}")
print(f"Final counts {Counter(ants)}")

# Plot initial and final distribution of ants
#plot_ant_distribution(initial_ants, ants, "Initial and Final Distribution of Ants")
