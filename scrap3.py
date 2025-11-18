import requests

url = "https://api.github.com/users/rajneesh75/repos"
r = requests.get(url)
repos = r.json()

for repo in repos:
    print(repo['name'], '-', repo['html_url'])