import os

from dotenv import load_dotenv


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")


if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN is not set in the .env file")
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

POST_TO_GITHUB = os.getenv("POST_TO_GITHUB", "false").lower() == "true"