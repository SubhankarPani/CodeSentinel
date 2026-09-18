from app.agents.base_agent import BaseAgent
from app.models.review import ReviewResult


class SecurityAgent(BaseAgent):
    """AI agent responsible for reviewing code for security vulnerabilities."""

    def __init__(self):
        super().__init__()

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

        result = self.invoke_with_retry(prompt)

        return result