from datetime import datetime, timedelta

import requests
from gh_activity_summarizer import config


class GithubAPI:
    def __init__(self, period=7):
        self.username = config.github_username
        self.token = config.github_token
        self.auth = (self.username, self.token)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period)
        self.start_date_str = start_date.strftime("%Y-%m-%d")
        self.end_date_str = end_date.strftime("%Y-%m-%d")

    def _get_results(self, response) -> list[dict[str, str]] | None:
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
            return res
        else:
            print(f"Failed to fetch {type}:", response.status_code, response.text)
            return None

    def _make_request(self, url, auth, params) -> requests.Response:
        response = requests.get(url, auth=auth, params=params)
        return response

    def print_results(self, response, type) -> None:
        if response.status_code == 200:
            items = response.json()["items"]
            for item in items:
                print(item["title"], item["html_url"], item["state"], item["body"])
                print("---------------------------------------------")
        else:
            print(f"Failed to fetch {type}:", response.status_code, response.text)

    def print_all_results(self) -> None:
        url = "https://api.github.com/search/issues"

        print(
            f"GitHub activity summary for {self.username} from {self.start_date_str} to {self.end_date_str}"
            f" (created or merged issues, reviewed PRs):"
        )

        print("=============================================")
        # Fetch created issues
        print("Created Issues:")
        created_issues_params = {
            "q": f"author:{self.username} type:issue created:{self.start_date_str}..{self.end_date_str}"
        }
        created_issues_response = self._make_request(url, self.auth, created_issues_params)
        self.print_results(created_issues_response, "issues")

        print("=============================================")

        # Fetch closed issues
        print("Closed Issues:")
        closed_issues_params = {
            "q": f"author:{self.username} type:issue closed:{self.start_date_str}..{self.end_date_str}"
        }
        closed_issues_response = self._make_request(url, self.auth, closed_issues_params)
        self.print_results(closed_issues_response, "issues")

        print("=============================================")

        print("Merged PRs:")
        # Fetch PRs
        merged_prs_params = {"q": f"author:{self.username} type:pr merged:{self.start_date_str}..{self.end_date_str}"}
        merged_prs_response = self._make_request(url, self.auth, merged_prs_params)
        self.print_results(merged_prs_response, "PRs")

        print("=============================================")

        print("Reviewed PRs:")
        # Fetch reviewed PRs
        review_params = {"q": f"reviewed-by:{self.username} type:pr updated:{self.start_date_str}..{self.end_date_str}"}
        review_response = self._make_request(url, self.auth, review_params)
        self.print_results(review_response, "reviewed PRs")

        print("=============================================")
        # Fetch involved PRs
        involved_prs_params = {
            "q": f"involves:{self.username} type:pr updated:{self.start_date_str}..{self.end_date_str}"
        }
        involved_prs_response = self._make_request(url, self.auth, involved_prs_params)
        self.print_results(involved_prs_response, "involved PRs")

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

    def get_github_activity_summary(self) -> dict[str, int]:
        url = "https://api.github.com/search/issues"

        created_issues_params = {
            "q": f"author:{self.username} type:issue created:{self.start_date_str}..{self.end_date_str}"
        }
        created_issues_response = self._make_request(url, self.auth, created_issues_params)

        closed_issues_params = {
            "q": f"author:{self.username} type:issue closed:{self.start_date_str}..{self.end_date_str}"
        }
        closed_issues_response = self._make_request(url, self.auth, closed_issues_params)

        merged_prs_params = {"q": f"author:{self.username} type:pr merged:{self.start_date_str}..{self.end_date_str}"}
        merged_prs_response = self._make_request(url, self.auth, merged_prs_params)

        review_params = {"q": f"reviewed-by:{self.username} type:pr updated:{self.start_date_str}..{self.end_date_str}"}
        review_response = self._make_request(url, self.auth, review_params)

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

    def get_all_github_activity(self) -> dict[str, list[dict[str, str]] | None]:
        url = "https://api.github.com/search/issues"

        created_issues_params = {
            "q": f"author:{self.username} type:issue created:{self.start_date_str}..{self.end_date_str}"
        }
        created_issues_response = self._make_request(url, self.auth, created_issues_params)
        created_issues = self._get_results(created_issues_response)

        closed_issues_params = {
            "q": f"author:{self.username} type:issue closed:{self.start_date_str}..{self.end_date_str}"
        }
        closed_issues_response = self._make_request(url, self.auth, closed_issues_params)
        closed_issues = self._get_results(closed_issues_response)

        merged_prs_params = {"q": f"author:{self.username} type:pr merged:{self.start_date_str}..{self.end_date_str}"}
        merged_prs_response = self._make_request(url, self.auth, merged_prs_params)
        merged_prs = self._get_results(merged_prs_response)

        review_params = {"q": f"reviewed-by:{self.username} type:pr updated:{self.start_date_str}..{self.end_date_str}"}
        review_response = self._make_request(url, self.auth, review_params)
        reviewed_prs = self._get_results(review_response)

        involved_prs_params = {
            "q": f"involves:{self.username} type:pr updated:{self.start_date_str}..{self.end_date_str}"
        }
        involved_prs_response = self._make_request(url, self.auth, involved_prs_params)
        involved_prs = self._get_results(involved_prs_response)

        return {
            "created_issues": created_issues,
            "closed_issues": closed_issues,
            "merged_prs": merged_prs,
            "reviewed_prs": reviewed_prs,
            "involved_prs": involved_prs,
        }
