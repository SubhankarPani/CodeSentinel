from app.agents.base_agent import BaseAgent
from app.models.review import ReviewResult


class StyleAgent(BaseAgent):
    """AI agent responsible for reviewing code style and quality."""

    def __init__(self):
        super().__init__()

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

        result = self.invoke_with_retry(prompt)

        return result