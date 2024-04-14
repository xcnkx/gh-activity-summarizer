import argparse

from gh_activity_summarizer.interfaces import github


def main(start_date=None, end_date=None):
    github_api = github.GithubAPI()
    github_api.print_all_results()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitHub Activity Summarizer")
    parser.add_argument("--start-date", help="Start date for fetching activity")
    parser.add_argument("--end-date", help="End date for fetching activity")
    args = parser.parse_args()

    main(args.start_date, args.end_date)
