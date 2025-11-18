import numpy as np
import pyswarm as pso
import random


class Solution:
    def __init__(self, name):
        self.name = name
        self.time_to_implement = 0.0
        self.cost_to_implement = 0.0
        self.efforts_to_implement = 0.0
        self.effectiveness = 0.0
        self.weights = [0.0, 0.0, 0.0, 0.0]

    def __repr__(self):
        return (f"Solution: {self.name}, "
                f"Time: {self.time_to_implement:.2f}, "
                f"Cost: {self.cost_to_implement:.2f}, "
                f"Efforts: {self.efforts_to_implement:.2f}, "
                f"Effectiveness: {self.effectiveness:.2f}, "
                f"Weights: {[f'{w:.2f}' for w in self.weights]}")


def objective_function(x):
    total_sum = 0.0
    for i in range(len(x) // 4):
        time = x[i * 4]
        cost = 1 / (time ** 2)
        efforts = x[i * 4 + 2]
        effectiveness = x[i * 4 + 3]
        total_sum += time + cost + efforts + effectiveness
    return total_sum


if __name__ == "__main__":

    solutions = [
        Solution("stop fossil fuels"),
        Solution("Plant more trees"),
        Solution("Carbon capture by technology"),
        Solution("Carbon capture by algae in oceans"),
        Solution("Reflecting back sunlight using technology")
    ]

    for solution in solutions:
        solution.weights = [round(random.uniform(1, 10), 2) for _ in range(4)]
        solution.time_to_implement = solution.weights[0]
        solution.cost_to_implement = solution.weights[1]
        solution.efforts_to_implement = solution.weights[2]
        solution.effectiveness = solution.weights[3]
        print(solution)

    num_solutions = len(solutions)
    print(num_solutions)
    num_parameters = 4

    lb = [1.0, 0.01, 1.0, 1.0] * num_solutions
    ub = [10.0, 10.0, 10.0, 10.0] * num_solutions

    print(lb)
    print(ub)

    optimal_weights, optimal_value = pso(objective_function ,lb, ub)
    print(optimal_weights)
    print(optimal_value)
