import time

from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GEMINI_API_KEY
from app.models.review import ReviewResult


class BaseAgent:
    """Base class for CodeSentinel AI agents."""

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash",
            google_api_key=GEMINI_API_KEY,
            temperature=0,
            timeout=60,
            max_retries=1
        )

        self.structured_llm = self.llm.with_structured_output(
            ReviewResult
        )

    def invoke_with_retry(
        self,
        prompt: str,
        max_retries: int = 3
    ):
        """Call Gemini and retry temporary failures."""

        for attempt in range(max_retries):

            try:

                print(
                    f"Calling Gemini "
                    f"(attempt {attempt + 1}/{max_retries})..."
                )

                # Show prompt size for debugging
                print(
                    f"Prompt characters: {len(prompt):,}"
                )

                # Approximate token count.
                # Rough estimate: 1 token ≈ 4 characters.
                estimated_tokens = len(prompt) // 4

                print(
                    f"Estimated input tokens: "
                    f"{estimated_tokens:,}"
                )

                print("Sending request to Gemini...")

                result = self.structured_llm.invoke(prompt)

                print("✅ Gemini response received.")

                return result

            except Exception as error:

                print("\n❌ Gemini request error:")
                print(f"Error type: {type(error).__name__}")
                print(f"Error message: {error}")
                print()

                error_message = str(error).lower()

                # --------------------------------------------------
                # QUOTA / RATE LIMIT
                # --------------------------------------------------

                if (
                    "quota" in error_message
                    or "429" in error_message
                    or "resource_exhausted" in error_message
                    or "too many requests" in error_message
                ):

                    raise RuntimeError(
                        "Gemini API quota/rate limit exceeded."
                    ) from error

                # --------------------------------------------------
                # LAST ATTEMPT
                # --------------------------------------------------

                if attempt == max_retries - 1:

                    print(
                        "❌ Maximum Gemini retry attempts reached."
                    )

                    raise

                # --------------------------------------------------
                # RETRY
                # --------------------------------------------------

                wait_time = 2 ** attempt

                print(
                    f"Gemini request failed. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)