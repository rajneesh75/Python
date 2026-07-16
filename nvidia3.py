import requests

r = requests.get(
    "https://integrate.api.nvidia.com",
    timeout=10
)

print(r.status_code)
print(r.text)