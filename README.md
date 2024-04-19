## Github Activity Summarizer

This is a simple python script that summarizes the activity of a github user. It uses the github API to get the user's activity and then summarizes it. The summary includes the number of commits, pull requests, issues, and comments made by the user. 

## Setup

1. Clone the repository
2. run `make setup`

## Usage

* Create a `.env` file in the root directory of the project and add the following:
```
GITHUB_USERNAME=<your_github_username>
GITHUB_TOKEN=<your_github_token>
ANTHROPIC_API_KEY=<your_anthropic_api_key>
```

* Run the scripts using the following command for a summary of your own activity on github summarized by LLM model(claude3):
```
python cli.py --period 1
```

* Others examples:

with other models:
```
python cli.py --period 1 --model claude-3-haiku-20240229
```

help:
```
❯ python cli.py -h
usage: cli.py [-h] [--period PERIOD] [--model MODEL] [--not-stream] [--without-llm]

GitHub Activity Summarizer with LLM

options:
  -h, --help       show this help message and exit
  --period PERIOD  Period for fetching activity in days
  --model MODEL    Model name for Claude
  --not-stream     Stream the output
  --without-llm    Only print the GitHub activity summary not using LLM

```
