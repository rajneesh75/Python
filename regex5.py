import re

text = "I love Python programming"
result = re.search("^Py", text)
print(result.group())