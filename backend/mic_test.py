import wave

import numpy as np
import sounddevice as sd


SAMPLE_RATE = 16000
CHANNELS = 1
RECORD_SECONDS = 5
OUTPUT_FILE = "backend/test_recording.wav"


def main():
    print("Microphone test")
    print(f"Recording for {RECORD_SECONDS} seconds...")
    print("Speak normally.")

    recording = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
    )

    sd.wait()

    print("Recording finished.")

    audio = np.asarray(recording, dtype=np.int16)

    with wave.open(OUTPUT_FILE, "wb") as wav_file:
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio.tobytes())

    print(f"Saved recording to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()