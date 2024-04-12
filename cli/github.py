import argparse
import os
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv


def main(username, token):
    # 認証情報を設定
    auth = (username, token)

    # 過去1週間の日付を計算
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # イシューを検索するAPIエンドポイントURLの設定
    issues_url = "https://api.github.com/search/issues"

    # リクエストパラメータ
    params = {"q": f"author:{username} type:issue created:{start_date_str}..{end_date_str}"}

    # APIリクエストを実行してデータを取得
    response = requests.get(issues_url, auth=auth, params=params)

    # 結果を確認
    if response.status_code == 200:
        issues = response.json()["items"]
        for issue in issues:
            print(issue["title"], issue["html_url"], issue["state"], issue["body"])
    else:
        print("Failed to fetch issues:", response.status_code, response.text)

    # プルリクエストを検索するAPIエンドポイントURLの設定
    prs_url = "https://api.github.com/search/issues"

    # リクエストパラメータ
    params = {"q": f"author:{username} type:pr merged:{start_date_str}..{end_date_str}"}

    # APIリクエストを実行してデータを取得
    response = requests.get(prs_url, auth=auth, params=params)

    # 結果を確認
    if response.status_code == 200:
        prs = response.json()["items"]
        for pr in prs:
            print(pr["title"], pr["html_url"], pr["state"], pr["body"])
    else:
        print("Failed to fetch PRs:", response.status_code, response.text)

    # レビューしたプルリクエストを検索するAPIエンドポイントURLの設定

    prs_url = "https://api.github.com/search/issues"

    # リクエストパラメータ
    params = {"q": f"reviewed-by:{username} type:pr updated:{start_date_str}..{end_date_str}"}

    # APIリクエストを実行してデータを取得
    response = requests.get(prs_url, auth=auth, params=params)

    # 結果を確認
    if response.status_code == 200:
        prs = response.json()["items"]
        for pr in prs:
            print(f"PR Title: {pr['title']}")
            print(f"PR URL: {pr['html_url']}")
            print(f"State: {pr['state']}")
            print(f"Created at: {pr['created_at']}")
            print(f"Merged: {'Yes' if pr.get('merged_at') else 'No'}")
            print("---")
    else:
        print("Failed to fetch PRs:", response.status_code, response.text)


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(description="GitHub Activity Summarizer")
    parser.add_argument("--username", required=True, help="GitHub username")
    parser.add_argument("--token", default=os.getenv("GITHUB_TOKEN"), help="GitHub personal access token")
    args = parser.parse_args()

    main(args.username, args.token)
