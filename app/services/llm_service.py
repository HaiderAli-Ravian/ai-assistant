from google import genai

from app.core.config import settings


client = genai.Client(api_key=settings.GOOGLE_API_KEY)


def generate_answer(prompt: str) -> str:
    """Generate a non-streaming answer using Gemini."""

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
    )

    return response.text or ""


def stream_answer(prompt: str):
    """Stream an answer from Gemini."""

    response_stream = client.models.generate_content_stream(
        model=settings.GEMINI_MODEL,
        contents=prompt,
    )

    for chunk in response_stream:
        if chunk.text:
            yield chunk.text