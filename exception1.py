# Function to divide two numbers and handle potential exceptions
def divide_numbers(a, b):
    try:
        result = a / b  # This might raise a ZeroDivisionError
        print(f"The result is: {result}")
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")
    except TypeError:
        print("Error: Invalid input type. Please enter numbers.")
    else:
        print("Division was successful.")
    finally:
        print("Execution of division is complete.")


# Test the function
divide_numbers(10, 2)  # Output: The result is: 5.0
#         Division was successful.
#         Execution of division is complete.

divide_numbers(10, 0)  # Output: Error: Cannot divide by zero.
#         Execution of division is complete.

divide_numbers(10, 'a')  # Output: Error: Invalid input type. Please enter numbers.
#         Execution of division is complete.
