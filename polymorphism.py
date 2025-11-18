# Base class 1
class Dog:
    def sound(self):
        return "Woof!"


# Base class 2
class Cat:
    def sound(self):
        return "Meow!"


# Base class 3
class Cow:
    def sound(self):
        return "Moo!"


# A function that demonstrates polymorphism
def animal_sound(animal):
    print(animal.sound())


# Creating objects of different types
dog = Dog()
cat = Cat()
cow = Cow()

# Calling the same method 'sound' on different objects
animal_sound(dog)  # Output: Woof!
animal_sound(cat)  # Output: Meow!
animal_sound(cow)  # Output: Moo!
