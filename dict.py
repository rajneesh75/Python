class Car:
    # Class attribute - generally NOT stored in __dict__ of instances
    wheels = 4

    def __init__(self, make, model, year):
        # Instance attributes - these ARE stored in the __dict__
        self.make = make
        self.model = model
        self.year = year
        self.engine_running = False

    def start_engine(self):
        self.engine_running = True
        print(f"The {self.make} {self.model}'s engine is now running.")

# --- Program Start ---

# 1. Create an instance of the class
my_car = Car("Toyota", "Camry", 2020)

print("### Initial Object State ###")
print(f"Object Type: {type(my_car)}")
print(f"Object Value: {my_car}")
print("-" * 30)

# 2. Access the __dict__ attribute
print("2. Accessing my_car.__dict__:")
print(my_car.__dict__)
# Output shows: {'make': 'Toyota', 'model': 'Camry', 'year': 2020, 'engine_running': False}

print("-" * 30)

# 3. Use __dict__ to modify an attribute
print("3. Modifying 'year' via __dict__:")
my_car.__dict__['year'] = 2021
print(f"Updated year (via normal access): {my_car.year}")

print("-" * 30)

# 4. Use __dict__ to add a new attribute dynamically
print("4. Adding a new attribute 'color' via __dict__:")
my_car.__dict__['color'] = 'Silver'
print(f"New attribute 'color' (via normal access): {my_car.color}")
print("my_car.__dict__ after addition:")
print(my_car.__dict__)

print("-" * 30)

# 5. Class __dict__ (stores class attributes and methods)
print("5. Car Class __dict__ (stores methods and class variables like 'wheels'):")
print(Car.__dict__)