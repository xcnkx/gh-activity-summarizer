import argparse

from gh_activity_summarizer.interfaces import claude, github


def print_activity_summary(stream=True, period=7):
    github_api = github.GithubAPI(period=period)

    github_activity = github_api.get_all_github_activity()
    github_summary = github_api.get_github_activity_summary()

    prompt = claude.get_prompt()
    llm_model = claude.get_claude_model()

    chain = prompt | llm_model

    if stream:
        for chunk in chain.stream(
            {
                "created_issues": github_activity["created_issues"],
                "closed_issues": github_activity["closed_issues"],
                "merged_prs": github_activity["merged_prs"],
                "reviewed_prs": github_activity["reviewed_prs"],
                "other_activity": github_activity["involved_prs"],
                "github_summary": github_summary,
            }
        ):
            print(chunk.content, end="", flush=True)
    else:
        print("Processing...")
        result = chain.invoke(
            {
                "created_issues": github_activity["created_issues"],
                "closed_issues": github_activity["closed_issues"],
                "merged_prs": github_activity["merged_prs"],
                "reviewed_prs": github_activity["reviewed_prs"],
                "other_activity": github_activity["involved_prs"],
                "github_summary": github_summary,
            },
            max_tokens=1024 * 4,
        )

        print("Result: \n", result.content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitHub Activity Summarizer with LLM")
    parser.add_argument("--period", help="Period for fetching activity", type=int, default=7)
    parser.add_argument("--not-stream", help="Stream the output", action="store_false")
    args = parser.parse_args()
    print_activity_summary(stream=args.not_stream, period=args.period)
