from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GEMINI_API_KEY
from app.models.review import ReviewResult


class LogicAgent:
    """AI agent responsible for reviewing code logic and correctness."""

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

        result = self.structured_llm.invoke(prompt)

        return result