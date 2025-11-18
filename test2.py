# Function to save user input to a file
def save_input_to_file(user_input):
    with open("user_input.txt", "a") as file:
        file.write(user_input + "\n")
        

# Function to suggest previous inputs from file
def suggest_previous_inputs():
    try:
        with open("user_input.txt", "r") as file:
            previous_inputs = file.readlines()
        print("Suggested previous inputs:")
        for idx, input_value in enumerate(previous_inputs, start=1):
            print(f"{idx}: {input_value.strip()}")
    except FileNotFoundError:
        print("No previous inputs found.")

# Example usage
def main():
    suggest_previous_inputs()
    user_input = input("Enter your input: ")
    save_input_to_file(user_input)

if __name__ == "__main__":
    main()
