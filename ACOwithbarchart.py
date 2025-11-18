import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib.animation as animation
from collections import Counter


def update_pheromone(pheromone, ants):
    print("\nupdate_pheromone")

    # Evaporate existing pheromone
    for path in pheromone:
        pheromone[path] = pheromone[path] * (1 - evaporation_rate)
    print(f"pheromone after evaporation {type(pheromone)} {pheromone}")

    # Deposits new pheromone only for paths that ants have visited
    for i in set(ants):
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

    # Handle division by zero in case total_pheromone is zero

    probabilities = []
    if total_pheromone == 0:
        probabilities = [1 / len(paths)] * len(paths)  # Uniform probability if no pheromone
    else:
        for level in pheromone_levels:
            probabilities.append(level / total_pheromone)
    print(f"probabilities: {probabilities}")

    # Update each ant's path based on pheromone probabilities
    for i in range(num_ants):
        ants[i] = random.choices(paths, probabilities)[0]
    print(f"Updated ants {type(ants)} {ants}")


def animate():
    # Update pheromone and ants for the current frame
    if iteration_count[0] < num_iterations:
        update_pheromone(pheromone, ants)
        update_ants(ants, pheromone)

        # Update the bar heights for the second set of bars
        final_count = Counter(ants)
        for i, solution in enumerate(solutions):
            target_height = final_count[solution]
            bars2[i].set_height(target_height)
            annotations2[i].set_text(f'{int(target_height)}')
            annotations2[i].set_position((bars2[i].get_x() + bars2[i].get_width() / 2, target_height))

        iteration_count[0] += 1
        # Update the displayed iteration count
        iteration_text.set_text(f'Iteration: {iteration_count[0]}')
    return bars2.patches + [iteration_text] + annotations2


# Annotate each bar with its value
def annotate_bars(bars, counts):
    annotations = []
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        annotation = ax.text(bar.get_x() + bar.get_width() / 2, height, f'{count}', ha='center', va='bottom')
        annotations.append(annotation)
    return annotations


if __name__ == "__main__":
    # Parameters
    num_ants = 10
    num_iterations = 10
    evaporation_rate = 0.1
    pheromone_deposit = 1.0
    paths = 5
    # Add a counter to track the number of iterations in the animation
    iteration_count = [0]

    # paths space
    paths_space = range(paths)

    # Initialize ants with random paths
    ants = []
    for _ in range(num_ants):
        ants.append(random.choice(paths_space))

    initial_ants = ants.copy()
    print(f"Initial ants {type(initial_ants)} {initial_ants}")
    print(f"Initial counts {Counter(initial_ants)}")

    # Initialize pheromone trails for each ant
    pheromone = {}
    for path in paths_space:
        pheromone[path] = 1

    print(f"pheromone {type(pheromone)} {pheromone}")

    initial_count = Counter(initial_ants)
    solutions = sorted(set(initial_count.keys()))

    initial_counts = []
    for solution in solutions:
        count = initial_count[solution]
        initial_counts.append(count)
    solutions = np.arange(len(solutions))

    fig, ax = plt.subplots()
    ax.set_xlabel('Solutions')
    ax.set_ylabel('Number of Ants')
    xticks = np.arange(paths)  # Adjust the range and step as needed
    ax.set_xticks(xticks)
    plt.ion()
    bar_width = 0.35

    bars1 = ax.bar(solutions - bar_width / 2, initial_counts, bar_width, color='blue', label='Initial')
    annotations1 = annotate_bars(bars1, initial_counts)

    final_count = Counter(ants)
    final_counts = []
    for solution in solutions:
        count = final_count[solution]
        final_counts.append(count)

    bars2 = ax.bar(solutions + bar_width / 2, final_counts, bar_width, color='orange', label="Final")
    annotations2 = annotate_bars(bars2, final_counts)
    yticks = np.arange(0, num_ants + 10, 1)  # Adjust the range and step as needed
    ax.set_yticks(yticks)

    ax.legend(loc='upper right')
    iteration_text = ax.text(0.95, -0.1, '', transform=ax.transAxes, ha='right', va='top')
    plt.tight_layout()

    # Create animation
    ani = animation.FuncAnimation(fig, animate, frames=num_iterations, interval=500, blit=False)
    plt.show(block=True)

    # Final paths
    print(f"\nInitial ants {type(initial_ants)} {initial_ants}")
    print(f"Initial counts {Counter(initial_ants)}")
    print(f"\nFinal ants {ants}")
    print(f"Final counts {Counter(ants)}")
