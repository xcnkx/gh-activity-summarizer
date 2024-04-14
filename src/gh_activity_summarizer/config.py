import os

from dotenv import load_dotenv

load_dotenv()

github_username = os.getenv("GITHUB_USERNAME")
github_token = os.getenv("GITHUB_TOKEN")

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
