# Simple Q-Learning Example in Python

import numpy as np
import random

# Environment setup
states = [0, 1, 2, 3, 4]  # positions
actions = ["left", "right"]  # possible moves
goal_state = 4

# Q-table (states x actions)
Q = np.zeros((len(states), len(actions)))

# Hyperparameters
learning_rate = 0.1
discount_factor = 0.9
epsilon = 0.2  # exploration rate
episodes = 200


# Reward function
def get_reward(state):
    return 10 if state == goal_state else -1


# Next state function
def step(state, action):
    if action == "left":
        next_state = max(0, state - 1)
    else:  # right
        next_state = min(len(states) - 1, state + 1)
    return next_state, get_reward(next_state)


# Q-Learning
for episode in range(episodes):
    state = 0  # start at position 0

    while state != goal_state:
        # Explore/exploit
        if random.uniform(0, 1) < epsilon:
            action_index = random.randint(0, 1)
        else:
            action_index = np.argmax(Q[state])

        action = actions[action_index]

        # Take action
        next_state, reward = step(state, action)

        # Q-learning update rule
        Q[state, action_index] = Q[state, action_index] + learning_rate * (
                reward + discount_factor * np.max(Q[next_state]) - Q[state, action_index]
        )

        state = next_state

print("Final Q-table:")
print(Q)

# Test the learned policy
state = 0
steps = [state]

while state != goal_state:
    action_index = np.argmax(Q[state])
    action = actions[action_index]
    state, _ = step(state, action)
    steps.append(state)

print("Learned path:", steps)
