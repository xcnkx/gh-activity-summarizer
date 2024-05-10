from gh_activity_summarizer.interfaces import claude, github


def print_activity_summary_with_llm(period, model_name, stream=True):
    github_api = github.GithubAPI(period=period)

    github_activity = github_api.get_all_github_activity()
    github_summary = github_api.get_github_activity_summary()

    prompt = claude.get_prompt()
    llm_model = claude.get_claude_model(model_name=model_name)

    chain = prompt | llm_model

    if stream:
        for chunk in chain.stream(
            {
                "created_issues": github_activity["created_issues"],
                "closed_issues": github_activity["closed_issues"],
                "merged_prs": github_activity["merged_prs"],
                "reviewed_prs": github_activity["reviewed_prs"],
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
            },
            max_tokens=1024 * 4,
        )

        print("Result: \n", result.content)

    print("\n\nSummary:")
    print("| Metric | Count |")
    print("|--------|-------|")
    print(f"| Total created issues | {github_summary['created_issues']} |")
    print(f"| Total closed issues | {github_summary['closed_issues']} |")
    print(f"| Total merged PRs | {github_summary['merged_prs']} |")
    print(f"| Total reviewed PRs | {github_summary['reviewed_prs']} |")


def print_acitivity_summary_without_llm(period: int):
    github_api = github.GithubAPI(period=period)
    github_api.print_all_results()
