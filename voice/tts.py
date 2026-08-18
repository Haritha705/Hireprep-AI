import os
import edge_tts


async def text_to_speech(
    text: str,
    output_path: str,
    voice: str = "en-IN-PrabhatNeural",
):
    """
    Convert text into speech.
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    communicate = edge_tts.Communicate(text, voice)

    await communicate.save(output_path)

    return output_path