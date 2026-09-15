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
            temperature=0
        )

        self.structured_llm = self.llm.with_structured_output(
            ReviewResult
        )

    def invoke_with_retry(self, prompt: str, max_retries: int = 3):
        """Call Gemini and retry temporary failures."""

        for attempt in range(max_retries):
            try:
                return self.structured_llm.invoke(prompt)

            except Exception as error:

                error_message = str(error).lower()

                # Quota errors will not be fixed by retrying.
                if "quota" in error_message or "429" in error_message:
                    raise RuntimeError(
                        "Gemini API quota exceeded."
                    ) from error

                # Retry temporary errors.
                if attempt == max_retries - 1:
                    raise error

                wait_time = 2 ** attempt

                print(
                    f"Gemini request failed. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)