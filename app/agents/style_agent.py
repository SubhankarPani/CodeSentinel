from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GEMINI_API_KEY


class StyleAgent:
    """AI agent responsible for reviewing code style and quality."""

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash",
            google_api_key=GEMINI_API_KEY,
            temperature=0,
        )

    def review(self, code_diff: str) -> str:

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

1. Severity: LOW, MEDIUM, or HIGH
2. File/line if identifiable
3. Explanation
4. Suggested improvement

If there are no style issues, say:

"No significant style issues found."

Code diff:

{code_diff}
"""

        response = self.llm.invoke(prompt)

        return response.content