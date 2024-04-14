from gh_activity_summarizer import config
from langchain.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic


def get_claude_model(model_name, temperature=0, max_tokens=1024 * 4):
    return ChatAnthropic(
        temperature=temperature, api_key=config.anthropic_api_key, model_name=model_name, max_tokens=max_tokens
    )


def get_prompt():
    prompt = PromptTemplate.from_template(
        """
こちらはあなたの過去1週間のGITHUBの活動をまとめた文章です。

## 作成したissues
---
{% for issues in created_issues %}
- [{{ issues.title }}]({{ issues.html_url }}): {{ issues.body }}
{% endfor %}

## クローズしたissues
---
{% for issues in closed_issues %}
- [{{ issues.title }}]({{ issues.html_url }}): {{ issues.body }}
{% endfor %}

## マージされたPR
---
{% for prs in merged_prs %}
- [{{ prs.title }}]({{ prs.html_url }}): {{ prs.body }}
{% endfor %}

## レビューしたPR
---
{% for prs in reviewed_prs %}
- [{{ prs.title }}]({{ prs.html_url }}): {{ prs.body }}
{% endfor %}

## 他に関わったIssueやPR
---
{% for activity in other_activity %}
- [{{ activity.title }}]({{ activity.html_url }}): {{ activity.body }}
{% endfor %}

## 総括
Total created issues: {{ github_summary.created_issues }}
Total closed issues: {{ github_summary.closed_issues }}
Total merged PRs: {{ github_summary.merged_prs }}
Total reviewed PRs: {{ github_summary.reviewed_prs }}


あなたはソフトウェアエンジニアです。上記のGITHUBの活動情報を元に、あなたの今週の活動を要約してください。
添付されたGitHubアクティビティのテキストを分析し、以下の項目に分けてmarkdown形式で要約してください。

## 作成したIssue
    * 新しく作成したIssueとその概要を1行で説明してください。
    * そのIssueのURLも記載してください。
    * 作成したIssueがない場合は「特になし」と記載してください。
## クローズしたIssueとPR
### クローズしたIssue
    * クローズしたIssueについて、その内容を1行で分かりやすく説明してください。
    * そのIssueのURLも記載してください。
    * クローズしたIssueがない場合は「特になし」と記載してください。
### マージされたPR
    * マージされたPRについて、その内容を1行で分かりやすく説明してください。
    * そのPRのURLも記載してください。
    * マージされたPRがない場合は「特になし」と記載してください。
## レビューしたPR
    * レビューを行ったPRについて、その内容を1行で要約してください。
    * そのPRのURLも記載してください。
    * レビューしたPRがない場合は「特になし」と記載してください。

## 他に関わったIssueやPR
* 上記以外で関わったIssueやPRがあれば、その内容を簡潔に説明してください。
* そのIssueやPRのURLも記載してください。
* 他に関わったIssueやPRがない場合は「特になし」と記載してください。

## 総括
全体的な活動内容について、以下の観点から総括を行ってください。
* コードの品質向上やシステムの効率化への貢献
""",  # noqa
        template_format="jinja2",
    )

    return prompt
