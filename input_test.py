import sys

# Print initial message and ask for input on the same line
sys.stdout.write("Enter your age: ")
sys.stdout.flush()  # Ensure that the output is printed immediately
age = input()  # Input occurs here

# Print another message on the same line after input
sys.stdout.write(f" Your age is {age}. Enter your name: ")
sys.stdout.flush()
name = input()  # Input occurs here

# Print the final output on the same line
sys.stdout.write(f" Hello, {name}!\n")
sys.stdout.flush()