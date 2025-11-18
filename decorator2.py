def decorator_function(original_function):
    def wrapper_function():
        print("Wrapper function adds this before the original function.")
        original_function()  # Calling the original function
        print("Wrapper function adds this after the original function.")
    return wrapper_function


@decorator_function
def hello():
    print('hello')


hello()





