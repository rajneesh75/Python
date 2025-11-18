from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader(".idea/templates"))

template = environment.get_template("message.txt")

max_score = 100
test_name = "Python Challenge"
students = [
    {"name": "Sandrine", "score": 100},
    {"name": "Gergeley", "score": 87},
    {"name": "Frieda", "score": 92},
    {"name": "Fritz", "score": 40},
    {"name": "Sirius", "score": 75},
]

for student in students:
    filename = f"message_{student['name'].lower()}.txt"
    content = template.render(student, max_score=max_score, test_name=test_name)
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"... wrote {filename}")