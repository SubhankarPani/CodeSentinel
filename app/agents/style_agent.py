from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GEMINI_API_KEY
from app.models.review import ReviewResult


class StyleAgent:
    """AI agent responsible for reviewing code style and quality."""

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash",
            google_api_key=GEMINI_API_KEY,
            temperature=0
        )

        self.structured_llm = self.llm.with_structured_output(
            ReviewResult
        )

    def review(self, code_diff: str) -> ReviewResult:

        prompt = f"""
You are a senior Python code reviewer.

Analyze the following GitHub Pull Request code diff.

Focus ONLY on code style and code quality.

Look for:
- Poor variable or function naming
- PEP 8 violations
- Poor readability
- Unnecessary complexity
- Duplicate code
- Bad formatting
- Poor coding practices

Do NOT report:
- Security vulnerabilities
- Business logic bugs
- Functional correctness issues

For every issue you find, provide:
- severity: LOW, MEDIUM, or HIGH
- category
- file
- line if identifiable
- description
- recommendation

If there are no significant style issues,
return an empty issues list.

Code diff:

{code_diff}
"""

        result = self.structured_llm.invoke(prompt)

        return result