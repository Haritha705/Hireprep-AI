import sounddevice as sd
import soundfile as sf
import os


class AudioRecorder:

    @staticmethod
    def record(
        filename="data/recordings/input.wav",
        duration=10,
        samplerate=16000
    ):

        os.makedirs("data/recordings", exist_ok=True)

        print("🎤 Recording...")

        audio = sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype="float32"
        )

        sd.wait()

        sf.write(filename, audio, samplerate)

        print(f"✅ Audio saved to {filename}")

        return filename


if __name__ == "__main__":
    AudioRecorder.record()