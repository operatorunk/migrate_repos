import requests

BITBUCKET_URL = "https://bitbucket.tuempresa.com"
USERNAME = "TU_USUARIO"
TOKEN = "TU_TOKEN"
PROJECT_KEY = "TU_PROJECT_KEY"


def get_paginated(url):
    results = []
    start = 0

    separator = "&" if "?" in url else "?"

    while True:
        paged_url = f"{url}{separator}start={start}"

        response = requests.get(
            paged_url,
            auth=(USERNAME, TOKEN),
            verify=False
        )

        response.raise_for_status()
        data = response.json()

        results.extend(data.get("values", []))

        if data.get("isLastPage", True):
            break

        start = data["nextPageStart"]

    return results


def get_repositories():
    url = f"{BITBUCKET_URL}/rest/api/1.0/projects/{PROJECT_KEY}/repos"
    return get_paginated(url)


def get_open_pull_requests(repo_slug):
    url = f"{BITBUCKET_URL}/rest/api/1.0/projects/{PROJECT_KEY}/repos/{repo_slug}/pull-requests"
    return get_paginated(f"{url}?state=OPEN")


def get_branches(repo_slug):
    url = f"{BITBUCKET_URL}/rest/api/1.0/projects/{PROJECT_KEY}/repos/{repo_slug}/branches"
    return get_paginated(url)


def main():
    repos = get_repositories()

    for repo in repos:
        repo_slug = repo["slug"]
        repo_name = repo["name"]

        open_prs = get_open_pull_requests(repo_slug)
        branches = get_branches(repo_slug)

        print("=" * 80)
        print(f"Repo: {repo_name} ({repo_slug})")

        print(f"\nOpen PRs: {len(open_prs)}")

        for pr in open_prs:
            author = pr.get("author", {}).get("user", {}).get("displayName", "N/A")

            print(
                f'  PR #{pr.get("id")} - {pr.get("title")} - Author: {author}'
            )

        print(f"\nBranches: {len(branches)}")

        for branch in branches:
            branch_name = branch.get("displayId", "N/A")
            latest_commit = branch.get("latestCommit", "N/A")

            print(
                f"  Branch: {branch_name} | Latest Commit: {latest_commit}"
            )


if __name__ == "__main__":
    main()
