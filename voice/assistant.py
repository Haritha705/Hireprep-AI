import asyncio
from voice.stt import speech_to_text
from voice.tts import text_to_speech


class VoiceAssistant:

    async def converse(self, audio_path: str):

        # STEP 1
        transcript = await speech_to_text(audio_path)

        # STEP 2
        from ai.llm_adapter import generate_text_with_langchain
        
        system_prompt = """
You are a professional AI Interviewer.

Be polite.

Ask interview questions.

Give short feedback.

Never answer unrelated questions.
"""
        ai_text = await asyncio.to_thread(
            generate_text_with_langchain,
            prompt=transcript,
            system_prompt=system_prompt.strip()
        )

        # STEP 3
        audio_output = "data/audio_output/reply.mp3"

        await text_to_speech(ai_text, audio_output)

        return {
            "transcript": transcript,
            "response": ai_text,
            "audio": audio_output
        }