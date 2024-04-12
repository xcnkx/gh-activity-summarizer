from datetime import datetime, timedelta

import requests


def calculate_dates():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    return start_date_str, end_date_str


def make_request(url, auth, params):
    response = requests.get(url, auth=auth, params=params)
    return response


def get_results(response):
    res = []
    if response.status_code == 200:
        items = response.json()["items"]
        for item in items:
            res.append(
                {
                    "title": item["title"],
                    "html_url": item["html_url"],
                    "state": item["state"],
                    "body": item["body"],
                }
            )
    else:
        return None


def print_results(response, type):
    if response.status_code == 200:
        items = response.json()["items"]
        for item in items:
            print(item["title"], item["html_url"], item["state"], item["body"])
            print("---------------------------------------------")
    else:
        print(f"Failed to fetch {type}:", response.status_code, response.text)


def print_all_results(username, token, start_date=None, end_date=None):
    auth = (username, token)

    if start_date and end_date:
        start_date_str = start_date
        end_date_str = end_date
    else:
        start_date_str, end_date_str = calculate_dates()

    url = "https://api.github.com/search/issues"

    print(
        f"GitHub activity summary for {username} from {start_date_str} to {end_date_str}"
        f" (created or merged issues, reviewed PRs):"
    )

    print("=============================================")
    # Fetch created issues
    print("Created Issues:")
    created_issues_params = {"q": f"author:{username} type:issue created:{start_date_str}..{end_date_str}"}
    created_issues_response = make_request(url, auth, created_issues_params)
    print_results(created_issues_response, "issues")

    print("=============================================")

    # Fetch closed issues
    print("Closed Issues:")
    closed_issues_params = {"q": f"author:{username} type:issue closed:{start_date_str}..{end_date_str}"}
    closed_issues_response = make_request(url, auth, closed_issues_params)
    print_results(closed_issues_response, "issues")

    print("=============================================")

    print("Merged PRs:")
    # Fetch PRs
    merged_prs_params = {"q": f"author:{username} type:pr merged:{start_date_str}..{end_date_str}"}
    merged_prs_response = make_request(url, auth, merged_prs_params)
    print_results(merged_prs_response, "PRs")

    print("=============================================")

    print("Reviewed PRs:")
    # Fetch reviewed PRs
    review_params = {"q": f"reviewed-by:{username} type:pr updated:{start_date_str}..{end_date_str}"}
    review_response = make_request(url, auth, review_params)
    print_results(review_response, "reviewed PRs")

    print("=============================================")
    # Fetch involved PRs
    involved_prs_params = {"q": f"involves:{username} type:pr updated:{start_date_str}..{end_date_str}"}
    involved_prs_response = make_request(url, auth, involved_prs_params)
    print_results(involved_prs_response, "involved PRs")

    # Print the summary of the activity
    print("=============================================")
    print("Summary:")
    created_issues_count = created_issues_response.json()["total_count"]
    closed_issues_count = closed_issues_response.json()["total_count"]
    merged_prs_count = merged_prs_response.json()["total_count"]
    reviewed_prs_count = review_response.json()["total_count"]
    print(f"Total created issues: {created_issues_count}")
    print(f"Total closed issues: {closed_issues_count}")
    print(f"Total merged PRs: {merged_prs_count}")
    print(f"Total reviewed PRs: {reviewed_prs_count}")


def get_github_activity_summary(username, token, start_date=None, end_date=None) -> dict:
    auth = (username, token)

    if start_date and end_date:
        start_date_str = start_date
        end_date_str = end_date
    else:
        start_date_str, end_date_str = calculate_dates()

    url = "https://api.github.com/search/issues"

    created_issues_params = {"q": f"author:{username} type:issue created:{start_date_str}..{end_date_str}"}
    created_issues_response = make_request(url, auth, created_issues_params)

    closed_issues_params = {"q": f"author:{username} type:issue closed:{start_date_str}..{end_date_str}"}
    closed_issues_response = make_request(url, auth, closed_issues_params)

    merged_prs_params = {"q": f"author:{username} type:pr merged:{start_date_str}..{end_date_str}"}
    merged_prs_response = make_request(url, auth, merged_prs_params)

    review_params = {"q": f"reviewed-by:{username} type:pr updated:{start_date_str}..{end_date_str}"}
    review_response = make_request(url, auth, review_params)

    created_issues_count = created_issues_response.json()["total_count"]
    closed_issues_count = closed_issues_response.json()["total_count"]
    merged_prs_count = merged_prs_response.json()["total_count"]
    reviewed_prs_count = review_response.json()["total_count"]

    return {
        "created_issues": created_issues_count,
        "closed_issues": closed_issues_count,
        "merged_prs": merged_prs_count,
        "reviewed_prs": reviewed_prs_count,
    }


def get_all_github_activity(username, token, start_date=None, end_date=None) -> dict:
    auth = (username, token)

    if start_date and end_date:
        start_date_str = start_date
        end_date_str = end_date
    else:
        start_date_str, end_date_str = calculate_dates()

    url = "https://api.github.com/search/issues"

    created_issues_params = {"q": f"author:{username} type:issue created:{start_date_str}..{end_date_str}"}
    created_issues_response = make_request(url, auth, created_issues_params)
    created_issues = get_results(created_issues_response)

    closed_issues_params = {"q": f"author:{username} type:issue closed:{start_date_str}..{end_date_str}"}
    closed_issues_response = make_request(url, auth, closed_issues_params)
    closed_issues = get_results(closed_issues_response)

    merged_prs_params = {"q": f"author:{username} type:pr merged:{start_date_str}..{end_date_str}"}
    merged_prs_response = make_request(url, auth, merged_prs_params)
    merged_prs = get_results(merged_prs_response)

    review_params = {"q": f"reviewed-by:{username} type:pr updated:{start_date_str}..{end_date_str}"}
    review_response = make_request(url, auth, review_params)
    reviewed_prs = get_results(review_response)

    involved_prs_params = {"q": f"involves:{username} type:pr updated:{start_date_str}..{end_date_str}"}
    involved_prs_response = make_request(url, auth, involved_prs_params)
    involved_prs = get_results(involved_prs_response)

    return {
        "created_issues": created_issues,
        "closed_issues": closed_issues,
        "merged_prs": merged_prs,
        "reviewed_prs": reviewed_prs,
        "involved_prs": involved_prs,
    }
