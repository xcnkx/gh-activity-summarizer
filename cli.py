import argparse

from gh_activity_summarizer.usecases import print_acitivity_summary_without_llm, print_activity_summary_with_llm


def main(args):
    if args.without_llm:
        print_acitivity_summary_without_llm(args.period)
    else:
        print_activity_summary_with_llm(args.period, args.model, args.not_stream)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitHub Activity Summarizer with LLM")
    parser.add_argument("--period", help="Period for fetching activity in days", type=int, default=7)
    parser.add_argument("--model", help="Model name for Claude", default="claude-3-opus-20240229")
    parser.add_argument("--not-stream", help="Stream the output", action="store_false")
    parser.add_argument(
        "--without-llm", help="Only print the GitHub activity summary not using LLM", action="store_true"
    )
    args = parser.parse_args()

    main(args)
