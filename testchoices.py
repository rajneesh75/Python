def display_menu(options):
    print("Select an option:")
    for key, value in options.items():
        print(f"{key}: {value}")


def get_user_choice(options):
    while True:
        display_menu(options)
        user_input = input("Enter the number of your choice: ")
        if user_input.isdigit() and int(user_input) in options:
            return int(user_input)
        else:
            print("Invalid input. Please enter a valid number.")


# Example list of choices
choices = {
    1: "Option 1",
    2: "Option 2",
    3: "Option 3"
}

# Get user's choice
user_choice = get_user_choice(choices)
print("You selected:", choices[user_choice])
