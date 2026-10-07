import json

from llm_client import generate_text


def generate_action_items(
    transcript: str,
    language: str = "English"
) -> dict:
    """
    Extract action items, deadlines, and open questions
    from a meeting transcript.

    Args:
        transcript: Meeting transcript as plain text.
        language: Output language for the generated content.

    Returns:
        A dictionary containing:
        - action_items
        - open_questions
    """

    prompt = f"""
You are an AI meeting assistant.

Analyze the following meeting transcript and extract actionable information.

Your tasks:
1. Identify all action items that were explicitly assigned or clearly stated.
2. Identify the person responsible for each action item when explicitly mentioned.
3. Identify the deadline for each action item when explicitly mentioned.
4. Identify unresolved questions or issues that still need clarification.

Rules:
- Use only information explicitly present in the transcript.
- Do not invent names, tasks, deadlines, or questions.
- If the responsible person is not mentioned, use "Not specified".
- If a deadline is not mentioned, use "Not specified".
- If there are no action items, return an empty list.
- If there are no open questions, return an empty list.
- Return exactly valid JSON.
- Do not add markdown or code fences.
- Generate the values/content in {language}.
- Keep the JSON keys exactly as specified below in English.

Use exactly this JSON structure:

{{
    "action_items": [
        {{
            "person": "Person name or Not specified",
            "task": "Task description",
            "deadline": "Deadline or Not specified"
        }}
    ],
    "open_questions": [
        "Question or unresolved issue"
    ]
}}

Meeting transcript:
{transcript}
"""

    response = generate_text(prompt)

    response = response.strip()

    # Remove accidental markdown code fences
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
    result.setdefault("action_items", [])
    result.setdefault("open_questions", [])

    return result