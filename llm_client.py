import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found.")


client = genai.Client(api_key=api_key)


def generate_text(
    prompt: str,
    model: str = "gemini-3.1-flash-lite"
) -> str:
    """
    Send a text prompt to Gemini and return the generated text.

    Args:
        prompt: Prompt to send to Gemini.
        model: Gemini model to use.

    Returns:
        Generated text.
    """

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    return response.text or ""