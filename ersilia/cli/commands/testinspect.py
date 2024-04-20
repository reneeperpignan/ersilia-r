import requests
import subprocess
import random

def getRepos():
    all_repos = []
    page = 1
    repos = []
    while True:
        params = {"page": page}
        url = f"https://api.github.com/orgs/ersilia-os/repos"
        headers = {"Accept": "application/vnd.github.v3+json"}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            if len(response.json()) == 0:
                break  # No more repositories to fetch
            for repo in response.json():
                if repo["name"][:3] == "eos":
                    repos.append(repo["name"])
            page += 1
        else:
            break
    print("Fetched ", len(repos), " repositories. Inspecting now.")
    return repos


repos = getRepos()
random.shuffle(repos)
for repo in repos:
    command = f"ersilia inspect {repo}"
    print(command)
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("Inspecting repo: ", repo)
    if result.returncode == 0:
        print("Output:")
        print(result.stdout)
    else:
        print("Error executing command:")
        print(result.stderr)
