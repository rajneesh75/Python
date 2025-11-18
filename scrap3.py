import requests

url = "https://api.github.com/users/octocat/repos"
r = requests.get(url)
repos = r.json()

for repo in repos:
    print(repo['name'], '-', repo['html_url'])