import requests
from requests.auth import HTTPBasicAuth

BITBUCKET_URL = "https://bitbucket.tuempresa.com"
USERNAME = "TU_USUARIO"
TOKEN = "TU_TOKEN"
PROJECT_KEY = "TU_PROJECT_KEY"


def get_projects():
    start = 0

    while True:
        url = f"{BITBUCKET_URL}/rest/api/1.0/projects?/{PROJECT_KEY}"

        response = requests.get(
            url,
            auth=HTTPBasicAuth(USERNAME, TOKEN),
            verify=False
        )

        response.raise_for_status()

        data = response.json()

        for project in data["values"]:
            print(
                f'{project["key"]} - {project["name"]}'
            )

        if data["isLastPage"]:
            break

        start = data["nextPageStart"]


if __name__ == "__main__":
    get_projects()
