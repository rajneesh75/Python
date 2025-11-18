# Base class (Parent)
class Vehicle:
    def __init__(self, make, model):
        self.make = make
        self.model = model

    def vehicle_info(self):
        return f"Vehicle: {self.make} {self.model}"

    def start(self):
        return f"The {self.make} {self.model} is starting."


# Derived class (Child) - Inherits from Vehicle
class Car(Vehicle):
    def __init__(self, make, model, doors):
        # Call the constructor of the parent class
        super().__init__(make, model)
        self.doors = doors  # Car-specific attribute

    # Car-specific method
    def car_info(self):
        return f"{self.make} {self.model} with {self.doors} doors"


# Creating an instance of the Car class
my_car = Car("Honda", "Civic", 4)

# Accessing methods from the parent class
print(my_car.vehicle_info())  # Output: Vehicle: Honda Civic
print(my_car.start())  # Output: The Honda Civic is starting.

# Accessing the method from the Car class
print(my_car.car_info())  # Output: Honda Civic with 4 doors
