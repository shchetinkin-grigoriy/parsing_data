import requests
import json
import re
from pprint import pprint
github_url = 'https://api.github.com'
user_name = 'shchetinkin-grigoriy'

# решил провести эксперимент с Regex
response = requests.get(github_url)
github_repos_url = response.json()["user_repositories_url"]
github_repos_url = re.search('^(.*)\{.+$', github_repos_url, re.IGNORECASE).group(1)
github_repos_url = github_repos_url.replace('{user}', user_name)
print(f'Repos url is: {github_repos_url}')

github_params = {"type": "all"}
response = requests.get(github_repos_url, params=github_params)
pprint(response.url)
github_data = response.json()
with open('homework_1_github.json','w') as f:
    json.dump(github_data, f)
