from app.agents.style_agent import StyleAgent
from app.agents.logic_agent import LogicAgent
from app.agents.security_agent import SecurityAgent


class ReviewService:
    """Coordinates all CodeSentinel review agents."""

    def __init__(self):
        self.style_agent = StyleAgent()
        self.logic_agent = LogicAgent()
        self.security_agent = SecurityAgent()

    def review(self, code_diff: str) -> dict:
        """Run all review agents and combine their results."""

        print("\nRunning Style Agent...")
        style_review = self.style_agent.review(code_diff)

        print("Running Logic Agent...")
        logic_review = self.logic_agent.review(code_diff)

        print("Running Security Agent...")
        security_review = self.security_agent.review(code_diff)

        return {
            "style": style_review,
            "logic": logic_review,
            "security": security_review,
        }