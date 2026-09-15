from app.agents.base_agent import BaseAgent
from app.models.review import ReviewResult


class LogicAgent(BaseAgent):
    """AI agent responsible for reviewing code logic and correctness."""

    def __init__(self):
        super().__init__()

    def review(self, code_diff: str) -> ReviewResult:

        prompt = f"""
You are a senior software engineer performing a code review.

Analyze the following GitHub Pull Request code diff.

Focus ONLY on logic, correctness, and potential functional bugs.

Look for:
- Incorrect conditions
- Incorrect calculations
- Incorrect control flow
- Edge cases
- Incorrect assumptions
- Off-by-one errors
- Incorrect handling of input or state
- Potential runtime errors
- Behavior that may produce incorrect results

Do NOT report:
- Code style issues
- Naming issues
- Formatting issues
- PEP 8 violations
- Security vulnerabilities

For every issue you find, provide:
- severity: LOW, MEDIUM, or HIGH
- category
- file
- line if identifiable
- description
- recommendation

Only report issues that are reasonably supported by the code.

If there are no significant logic or correctness issues,
return an empty issues list.

Code diff:

{code_diff}
"""

        result = self.invoke_with_retry(prompt)

        return result