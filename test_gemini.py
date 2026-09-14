from google import genai
from app.config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Say hello to CodeSentinel in one sentence."
)

print(response.text)