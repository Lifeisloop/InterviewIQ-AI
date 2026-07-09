from ollama import chat


MODEL_NAME = "llama3.2"


def ask_llm(prompt: str) -> str:
    """
    Send a prompt to the local Ollama model
    and return the generated text response.
    """

    if not prompt or not prompt.strip():
        raise ValueError(
            "Prompt cannot be empty."
        )

    try:
        response = chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt.strip()
                }
            ],
            format="json"
        )

        content = response["message"]["content"]

        if not content:
            raise ValueError(
                "Ollama returned an empty response."
            )

        return content.strip()

    except Exception as error:
        print(
            "OLLAMA ERROR:",
            str(error)
        )

        raise RuntimeError(
            f"Failed to generate AI response: {error}"
        ) from error