numbers = (4, 7, 19, 2, 89, 45, 72, 22)
sorted_numbers = sorted(numbers)
print(sorted_numbers)
even = lambda a: a % 2 == 0

even_numbers = filter(even, sorted_numbers)
print(type(even_numbers))
 
