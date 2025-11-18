# Defining the Car class
class Car:
    # Constructor to initialize attributes
    def __init__(self, make, model, year):
        self.make = make  # Car's manufacturer
        self.model = model  # Car's model
        self.year = year  # Car's manufacturing year

    # Method to display car details
    def car_info(self):
        return f"{self.year} {self.make} {self.model}"

    # Method to simulate starting the car
    def start(self):
        return f"The {self.make} {self.model} is now starting."


# Creating an instance of the Car class
my_car = Car("Toyota", "Corolla", 2020)

# Accessing methods
print(my_car.car_info())  # Output: 2020 Toyota Corolla
print(my_car.start())  # Output: The Toyota Corolla is now starting.
