from typing import Any

from langchain_core.tools import tool

from voice.assistant import VoiceAssistant


@tool
async def voice_tool(audio_path: str) -> dict[str, Any]:
    """Wrap the existing voice assistant workflow as a LangChain tool."""
    try:
        assistant = VoiceAssistant()
        result = await assistant.converse(audio_path)
        return {
            "status": "success",
            "data": result,
        }
    except Exception as exc:
        return {
            "status": "error",
            "error": f"Voice workflow failed: {exc}",
        }
