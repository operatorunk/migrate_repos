import requests
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BITBUCKET_URL = "https://bitbucket.tuempresa.com"
USERNAME = "TU_USUARIO"
TOKEN = "TU_TOKEN"
PROJECT_KEY = "TU_PROJECT_KEY"

STALE_BRANCH_DAYS = 180


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


def format_timestamp(timestamp_ms):
    if not timestamp_ms:
        return "N/A"

    return datetime.fromtimestamp(timestamp_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")


def timestamp_to_datetime(timestamp_ms):
    if not timestamp_ms:
        return None

    return datetime.fromtimestamp(timestamp_ms / 1000)


def get_repositories():
    url = f"{BITBUCKET_URL}/rest/api/1.0/projects/{PROJECT_KEY}/repos"
    return get_paginated(url)


def get_open_pull_requests(repo_slug):
    url = f"{BITBUCKET_URL}/rest/api/1.0/projects/{PROJECT_KEY}/repos/{repo_slug}/pull-requests?state=OPEN"
    return get_paginated(url)


def get_branches(repo_slug):
    url = f"{BITBUCKET_URL}/rest/api/1.0/projects/{PROJECT_KEY}/repos/{repo_slug}/branches"
    return get_paginated(url)


def get_tags(repo_slug):
    url = f"{BITBUCKET_URL}/rest/api/1.0/projects/{PROJECT_KEY}/repos/{repo_slug}/tags"
    return get_paginated(url)


def get_commit(repo_slug, commit_id):
    url = f"{BITBUCKET_URL}/rest/api/1.0/projects/{PROJECT_KEY}/repos/{repo_slug}/commits/{commit_id}"

    response = requests.get(
        url,
        auth=(USERNAME, TOKEN),
        verify=False
    )

    response.raise_for_status()
    return response.json()


def get_default_branch_from_branches(branches):
    for branch in branches:
        if branch.get("isDefault") is True:
            return branch.get("displayId", "N/A")

    return "N/A"


def get_repo_size(repo):
    size = repo.get("size")

    if size is None:
        return "N/A"

    return size


def is_stale_branch(commit_datetime):
    if not commit_datetime:
        return False

    age_days = (datetime.now() - commit_datetime).days
    return age_days > STALE_BRANCH_DAYS


def main():
    repos = get_repositories()

    for repo in repos:
        repo_slug = repo["slug"]
        repo_name = repo["name"]
        repo_size = get_repo_size(repo)

        open_prs = get_open_pull_requests(repo_slug)
        branches = get_branches(repo_slug)
        default_branch = get_default_branch_from_branches(branches)
        tags = get_tags(repo_slug)

        latest_repo_activity = None

        print("=" * 80)
        print(f"Repo: {repo_name} ({repo_slug})")
        print(f"Default Branch: {default_branch}")
        print(f"Repo Size: {repo_size}")
        print(f"Tags: {len(tags)}")

        print(f"\nOpen PRs: {len(open_prs)}")

        for pr in open_prs:
            author = pr.get("author", {}).get("user", {}).get("displayName", "N/A")
            from_branch = pr.get("fromRef", {}).get("displayId", "N/A")
            to_branch = pr.get("toRef", {}).get("displayId", "N/A")

            print(
                f'  PR #{pr.get("id")} - {pr.get("title")} | '
                f'Author: {author} | '
                f'From: {from_branch} | '
                f'To: {to_branch}'
            )

        print(f"\nBranches: {len(branches)}")

        for branch in branches:
            branch_name = branch.get("displayId", "N/A")
            latest_commit = branch.get("latestCommit", "N/A")

            commit = get_commit(repo_slug, latest_commit)

            author = commit.get("author", {}).get("name", "N/A")
            author_email = commit.get("author", {}).get("emailAddress", "N/A")
            commit_timestamp = commit.get("authorTimestamp")
            commit_date = format_timestamp(commit_timestamp)
            commit_datetime = timestamp_to_datetime(commit_timestamp)

            if commit_datetime and (
                latest_repo_activity is None or commit_datetime > latest_repo_activity
            ):
                latest_repo_activity = commit_datetime

            stale_status = "STALE" if is_stale_branch(commit_datetime) else "ACTIVE"

            print(
                f"  Branch: {branch_name} | "
                f"Latest Commit: {latest_commit} | "
                f"Author: {author} | "
                f"Email: {author_email} | "
                f"Date: {commit_date} | "
                f"Status: {stale_status}"
            )

        latest_repo_activity_text = (
            latest_repo_activity.strftime("%Y-%m-%d %H:%M:%S")
            if latest_repo_activity
            else "N/A"
        )

        print(f"\nLatest Repo Activity: {latest_repo_activity_text}")

        if tags:
            print("\nTags:")
            for tag in tags:
                tag_name = tag.get("displayId", "N/A")
                latest_commit = tag.get("latestCommit", "N/A")
                print(f"  Tag: {tag_name} | Commit: {latest_commit}")


if __name__ == "__main__":
    main()
