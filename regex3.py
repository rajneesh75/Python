import re

text = "cat, mat, bat, rat"
result = re.findall("[cb]at", text)
print(result)