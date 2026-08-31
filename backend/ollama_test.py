import ollama


MODEL = "qwen3.5:4b"


def main():
    print("Sending request to Ollama...")

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: Nova is online."
            }
        ],
    )

    message = response["message"]["content"]

    print("\nOllama response:")
    print(message)


if __name__ == "__main__":
    main()