from jinja2 import Template

# Define the template as a string
template1 = Template("Hello, {{ name }}! You have {{ notifications }} new notifications.")
template2 = Template("Hello, {{ name | upper }}!")

# Render the template with data
rendered_template1 = template1.render(name="Alice", notifications=5)
print(rendered_template1)

# Render the template with data
rendered_template2 = template2.render(name="Alice")
print(rendered_template2)
