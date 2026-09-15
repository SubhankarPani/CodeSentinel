
from app.agents.style_agent import StyleAgent
from app.agents.logic_agent import LogicAgent
from app.agents.security_agent import SecurityAgent
from app.agents.review_agent import ReviewAgent


class ReviewService:
    """Coordinates all CodeSentinel review agents."""

    def __init__(self):
        self.style_agent = StyleAgent()
        self.logic_agent = LogicAgent()
        self.security_agent = SecurityAgent()
        self.review_agent = ReviewAgent()

    def review(self, code_diff: str) -> dict:
        """Run all review agents and create a final review."""

        try:
            print("\nRunning Style Agent...")
            style_review = self.style_agent.review(code_diff)

            print("Running Logic Agent...")
            logic_review = self.logic_agent.review(code_diff)

            print("Running Security Agent...")
            security_review = self.security_agent.review(code_diff)

            print("Running Review Agent...")
            final_review = self.review_agent.review(
                style_review,
                logic_review,
                security_review
            )

            return {
                "style": style_review,
                "logic": logic_review,
                "security": security_review,
                "final": final_review,
            }

        except Exception as e:
            error_message = str(e)

            if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                print("\n" + "=" * 50)
                print("❌ CODESENTINEL REVIEW FAILED")
                print("=" * 50)
                print("\nReason: Gemini API quota exceeded.")
                print("Please wait for your free quota to reset.")
                print("=" * 50)

            else:
                print("\n" + "=" * 50)
                print("❌ CODESENTINEL REVIEW FAILED")
                print("=" * 50)
                print(f"\nError: {error_message}")
                print("=" * 50)

            return {}