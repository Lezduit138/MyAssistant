from faster_whisper import WhisperModel


MODEL_SIZE = "base"
AUDIO_FILE = "backend/test_recording.wav"


def main():
    print("Loading Whisper model...")

    model = WhisperModel(
        MODEL_SIZE,
        device="cpu",
        compute_type="int8",
    )

    print("Transcribing audio...")

    segments, info = model.transcribe(
    AUDIO_FILE,
    language="en",
    beam_size=5,
)

    print("\nDetected language:", info.language)
    print("Language probability:", info.language_probability)

    print("\nTranscription:")

    text_parts = []

    for segment in segments:
        text = segment.text.strip()

        if text:
            text_parts.append(text)
            print(text)

    full_text = " ".join(text_parts)

    print("\nFinal text:")
    print(full_text)


if __name__ == "__main__":
    main()