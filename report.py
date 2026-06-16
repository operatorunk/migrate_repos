import requests

BITBUCKET_URL = "https://bitbucket.tuempresa.com"
USERNAME = "TU_USUARIO"
TOKEN = "TU_TOKEN"
PROJECT_KEY = "TU_PROJECT_KEY"


def get_repositories():
    start = 0

    while True:
        url = f"{BITBUCKET_URL}/rest/api/1.0/projects/{PROJECT_KEY}/repos?start={start}"

        response = requests.get(
            url,
            auth=(USERNAME, TOKEN),
            verify=False
        )

        response.raise_for_status()
        data = response.json()

        for repo in data["values"]:
            print(f'{PROJECT_KEY} - {repo["slug"]} - {repo["name"]}')

        if data["isLastPage"]:
            break

        start = data["nextPageStart"]


if __name__ == "__main__":
    get_repositories()
