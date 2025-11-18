import re

text = "Python is fun"
result = re.match("Python", text)

if result:
    print("Match found:", result.group())
else:
    print("No match")