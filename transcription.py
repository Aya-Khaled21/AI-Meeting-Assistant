import os
import tempfile

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found.")

client = genai.Client(api_key=api_key)


def transcribe_audio(audio_file) -> str:
    """
    Transcribe an uploaded audio or video file into text.

    Args:
        audio_file: Streamlit uploaded audio or video file.

    Returns:
        The transcript as a string.
    """

    file_extension = os.path.splitext(audio_file.name)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=file_extension,
    ) as temp_file:

        temp_file.write(audio_file.getbuffer())
        temp_file_path = temp_file.name

    try:
        uploaded_file = client.files.upload(file=temp_file_path)

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[
                (
                    "Transcribe this meeting recording exactly into text. "
                    "The uploaded file may be audio or video. "
                    "Return only the spoken transcript. "
                    "Do not summarize or analyze the content."
                ),
                uploaded_file,
            ],
        )

        return response.text or ""

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)