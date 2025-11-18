import random
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np


# Plot initial and final distribution of preferences
def plot_distribution(initial, final, title):
    initial_count = Counter(initial)
    final_count = Counter(final)

    solution_names = list(support.keys())
    initial_counts = [initial_count[solution] for solution in solution_names]
    final_counts = [final_count[solution] for solution in solution_names]

    bar_width = 0.35
    index = np.arange(len(solution_names))

    plt.bar(index, initial_counts, bar_width, color='b', label='Initial')
    plt.bar(index + bar_width, final_counts, bar_width, color='r', label='Final')

    plt.xlabel('Solutions')
    plt.ylabel('Number of People')
    plt.title(title)
    plt.xticks(index + bar_width / 2, solution_names)
    plt.legend()
    plt.show()


def update_support(support, preferences):
    print("\nupdate support module")
    # Evaporate existing support
    for solution in support:
        support[solution] = support[solution] * (1 - evaporation_rate)

    # Deposit new support based on current preferences
    for solution in preferences:
        support[solution] = support[solution] + support_increment
    print(f"Updated support {type(support)} {support}")


def update_preferences(preferences, support):
    print("\nupdate preferences module")

    solutions = list(support.keys())
    support_levels = list(support.values())
    total_support = sum(support_levels)

    probabilities = []
    for level in support_levels:
        probability = level / total_support
        probabilities.append(probability)

    print(f"Assigning new preferences")
    for i in range(num_people):
        preferences[i] = random.choices(solutions, probabilities)[0]
    print(f"Updated preferences {type(preferences)} {preferences}")


# Parameters
num_people = 10
num_iterations = 1
evaporation_rate = 0.1
support_increment = 1.0
solutions = ['Solution 1', 'Solution 2', 'Solution 3', 'Solution 4', 'Solution 5']

# Initialize each person's preferences
preferences = []
for _ in range(num_people):
    choice = random.choice(solutions)
    preferences.append(choice)

print(f"Initial preferences {type(preferences)} {preferences}")
initial_preferences = preferences.copy()

# Initialize support levels for each solution
support = {}
for solution in solutions:
    support[solution] = 1
print(f"support {type(support)} {support}")

for iteration in range(num_iterations):
    update_support(support, preferences)
    update_preferences(preferences, support)

# Final support levels
print(f"\nInitial preferences: {Counter(initial_preferences)}")
print(f"Final preferences: {Counter(preferences)}")
# print(f"Support levels:      {support}")
# plot_distribution(initial_preferences, preferences, "Initial and Final Distribution of Preferences")
