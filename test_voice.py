"""
Voice Layer Test Script
========================
Tests the full pipeline: STT -> LLM -> TTS via POST /voice

Run:
    python test_voice.py

Requirements: server must be running (uvicorn main:app --reload)
"""

import os
import struct
import wave
import requests

BASE_URL = "http://localhost:8000"
TEST_AUDIO_PATH = "test_input.wav"


# -------------------------------------------------------
# Step 1: Create a short silent WAV file for testing STT
#         (Replace this file with a real recording to get
#          a meaningful transcript from Groq Whisper)
# -------------------------------------------------------
def create_test_wav(path: str, duration_sec: float = 3.0, sample_rate: int = 16000):
    """Create a minimal valid WAV file (silent audio) for testing."""
    num_samples = int(duration_sec * sample_rate)
    audio_data = struct.pack("<" + "h" * num_samples, *([0] * num_samples))  # silence

    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)        # Mono
        wf.setsampwidth(2)        # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data)

    print(f"[1] Created test WAV: {path} ({duration_sec}s, {sample_rate}Hz)")


# -------------------------------------------------------
# Step 2: POST to /voice endpoint
# -------------------------------------------------------
def test_voice_endpoint(audio_path: str):
    print(f"\n[2] POSTing {audio_path} to {BASE_URL}/voice ...")

    with open(audio_path, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/voice",
            files={"audio": (os.path.basename(audio_path), f, "audio/wav")},
            timeout=60
        )

    if response.status_code != 200:
        print(f"[ERROR] HTTP {response.status_code}: {response.text}")
        return None

    data = response.json()
    return data


# -------------------------------------------------------
# Step 3: Validate results
# -------------------------------------------------------
def validate(data: dict):
    result = data.get("response", {})

    transcript = result.get("transcript", "")
    llm_reply  = result.get("response", "")
    audio_out  = result.get("audio", "")

    print("\n========== VOICE PIPELINE RESULT ==========")
    print(f"[STT] Transcript : {transcript!r}")
    print(f"[LLM] AI Response: {llm_reply!r}")
    print(f"[TTS] Audio file : {audio_out}")

    # Check TTS file was created
    if os.path.exists(audio_out):
        size = os.path.getsize(audio_out)
        print(f"[TTS] OK Audio file exists ({size} bytes)")
    else:
        print(f"[TTS] FAIL Audio file NOT found at: {audio_out}")

    # Basic assertions
    assert isinstance(transcript, str), "STT transcript must be a string"
    assert isinstance(llm_reply, str) and len(llm_reply) > 0, "LLM reply must be non-empty"
    assert os.path.exists(audio_out), "TTS output audio file must exist"

    print("\n[PASS] ALL CHECKS PASSED -- Voice pipeline is working correctly!")


# -------------------------------------------------------
# Main
# -------------------------------------------------------
if __name__ == "__main__":
    # Use a real WAV if you have one, else generate silent test file
    real_audio = None  # Set to e.g. "my_voice.wav" if you have one

    audio_to_use = real_audio if real_audio else TEST_AUDIO_PATH

    if not real_audio:
        create_test_wav(TEST_AUDIO_PATH)

    data = test_voice_endpoint(audio_to_use)

    if data:
        validate(data)

    # Cleanup
    if os.path.exists(TEST_AUDIO_PATH):
        os.remove(TEST_AUDIO_PATH)
