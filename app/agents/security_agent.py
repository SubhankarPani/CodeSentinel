from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GEMINI_API_KEY
from app.models.review import ReviewResult


class SecurityAgent:
    """AI agent responsible for reviewing code for security vulnerabilities."""

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
You are a senior application security engineer.

Analyze the following GitHub Pull Request code diff.

Focus ONLY on security vulnerabilities.

Look for:
- Hardcoded passwords, API keys, tokens, or secrets
- SQL injection
- Command injection
- Path traversal
- Unsafe use of eval() or exec()
- Insecure deserialization
- Unsafe file operations
- Authentication vulnerabilities
- Authorization vulnerabilities
- Sensitive information exposure
- Improper input validation
- Other realistic security vulnerabilities

Do NOT report:
- Code style issues
- Naming issues
- Formatting issues
- PEP 8 violations
- General performance issues
- General business logic bugs

Only report security issues that are reasonably supported by
the code in the diff.

For every security issue you find, provide:
- severity: LOW, MEDIUM, or HIGH
- category
- file
- line if identifiable
- description
- recommendation

If there are no significant security vulnerabilities,
return an empty issues list.

Code diff:

{code_diff}
"""

        result = self.structured_llm.invoke(prompt)

        return result