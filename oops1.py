class Car:
    def __init__(self, brand, model):  # Constructor
        self.brand = brand
        self.model = model

    def start(self):  # Method
        print(f"{self.brand} {self.model} is starting...")


# Create object (instance)
car1 = Car("Toyota", "Fortuner")
car1.start()
