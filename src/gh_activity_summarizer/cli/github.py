import argparse
from datetime import datetime, timedelta

import requests


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
            print(issue["title"], issue["html_url"], issue["state"])
    else:
        print("Failed to fetch issues:", response.status_code, response.text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitHub Activity Summarizer")
    parser.add_argument("--username", required=True, help="GitHub username")
    parser.add_argument("--token", required=True, help="GitHub personal access token")
    args = parser.parse_args()

    main(args.username, args.token)
