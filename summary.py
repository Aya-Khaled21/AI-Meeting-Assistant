import json

from llm_client import generate_text


def generate_summary(
    transcript: str,
    language: str = "English"
) -> dict:
    """
    Generate a structured summary from a meeting transcript.

    Args:
        transcript: Meeting transcript as plain text.
        language: Output language for the generated content.

    Returns:
        A dictionary containing:
        - summary
        - key_points
        - decisions
    """

    prompt = f"""
You are an AI meeting assistant.

Analyze the following meeting transcript and extract the most important information.

Your tasks:
1. Write a concise meeting summary.
2. Identify the key discussion points.
3. Identify the decisions that were made.

Rules:
- Use only information explicitly mentioned in the transcript.
- Do not invent names, facts, decisions, or details.
- Keep the summary concise and clear.
- Return exactly valid JSON.
- Do not add markdown or code fences.
- Generate the values/content in {language}.
- Keep the JSON keys exactly as specified below in English.

Use this exact JSON structure:

{{
    "summary": "A concise summary of the meeting",
    "key_points": [
        "Key discussion point 1",
        "Key discussion point 2"
    ],
    "decisions": [
        "Decision 1",
        "Decision 2"
    ]
}}

Meeting transcript:
{transcript}
"""

    response = generate_text(prompt)

    # Remove accidental markdown code fences
    response = response.strip()

    if response.startswith("```json"):
        response = response[7:]

    if response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()

    try:
        result = json.loads(response)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Gemini returned invalid JSON:\n{response}"
        ) from e

    # Make sure the expected keys exist
    result.setdefault("summary", "")
    result.setdefault("key_points", [])
    result.setdefault("decisions", [])

    return result