from collections import namedtuple

# Define a namedtuple called 'Point'
Point = namedtuple('Point', ['x', 'y'])

# Create an instance of Point
p = Point(10, 20)

# Access the fields
print(p.x)  # Output: 10
print(p.y)  # Output: 20
