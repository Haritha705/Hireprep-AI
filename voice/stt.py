import os
import litellm
import config


async def speech_to_text(audio_path: str) -> str:
    """
    Convert speech to text using Groq Whisper.
    """

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    with open(audio_path, "rb") as audio_file:
        response = await litellm.atranscription(
            model="groq/whisper-large-v3-turbo",
            file=audio_file,
            api_key=config.GROQ_API_KEY,
        )

    return response.text