from app.agents.base_agent import BaseAgent
from app.models.review import ReviewResult


class ReviewAgent(BaseAgent):
    """AI agent responsible for creating the final combined review."""

    def __init__(self):
        super().__init__()

    def review(
        self,
        style_review: ReviewResult,
        logic_review: ReviewResult,
        security_review: ReviewResult
    ) -> ReviewResult:

        prompt = f"""
You are the senior reviewer responsible for creating the final
code review.

You have received findings from three specialized reviewers:

STYLE REVIEW:
{style_review.model_dump_json(indent=2)}

LOGIC REVIEW:
{logic_review.model_dump_json(indent=2)}

SECURITY REVIEW:
{security_review.model_dump_json(indent=2)}

Your job is to combine these findings into one final review.

Rules:

1. Remove duplicate or overlapping findings.
2. Keep the most important version of duplicate findings.
3. Preserve the correct severity.
4. Do not invent new issues.
5. Keep only findings supported by the reviewers.
6. Make descriptions concise and easy to understand.
7. Make recommendations practical and actionable.
8. Preserve the file and line information when available.

Return the final review using the ReviewResult format.
"""

        result = self.invoke_with_retry(prompt)

        return result