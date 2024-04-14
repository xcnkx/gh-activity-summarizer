## Github Activity Summarizer

This is a simple python script that summarizes the activity of a github user. It uses the github API to get the user's activity and then summarizes it. The summary includes the number of commits, pull requests, issues, and comments made by the user. 

## Setup

1. Clone the repository
2. run `make setup`

## Usage

1. Create a `.env` file in the root directory of the project and add the following:
```
GITHUB_USERNAME=<your_github_username>
GITHUB_TOKEN=<your_github_token>
ANTHROPIC_API_KEY=<your_anthropic_api_key>
```

2. Run the scripts using the following command for a summary of your own activity on github summarized by LLM model(claude3):
```
make run/llm
``` 
