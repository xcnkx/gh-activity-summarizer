import argparse
import os

from dotenv import load_dotenv
from gh_activity_summarizer import github


def main(username, token, start_date=None, end_date=None):
    github.print_all_results(username, token, start_date, end_date)


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(description="GitHub Activity Summarizer")
    parser.add_argument("--username", required=True, help="GitHub username")
    parser.add_argument("--token", default=os.getenv("GITHUB_TOKEN"), help="GitHub personal access token")
    parser.add_argument("--start-date", help="Start date for fetching activity")
    parser.add_argument("--end-date", help="End date for fetching activity")
    args = parser.parse_args()

    main(args.username, args.token, args.start_date, args.end_date)
