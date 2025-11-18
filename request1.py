import requests

response = requests.get("https://api.github.com")
print(response.status_code)
print(response.headers['content-type'])
print(response.text[:200])  # print first 200 chars