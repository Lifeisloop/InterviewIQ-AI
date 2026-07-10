import os

from ollama import chat
from openai import OpenAI


LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "ollama"
).lower()


def ask_llm(prompt: str) -> str:
    """
    Send prompt to configured LLM provider.

    Local:
        LLM_PROVIDER=ollama

    Production Options:
        LLM_PROVIDER=openai
        LLM_PROVIDER=groq
    """

    if LLM_PROVIDER == "openai":
        return ask_openai(prompt)
    elif LLM_PROVIDER == "groq":
        return ask_groq(prompt)

    return ask_ollama(prompt)


def ask_ollama(prompt: str) -> str:
    """
    Use local Ollama model.
    """

    response = chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format="json"
    )

    return response["message"]["content"]


def ask_openai(prompt: str) -> str:
    """
    Use OpenAI API for cloud deployment.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not configured."
        )

    client = OpenAI(
        api_key=api_key
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI interview evaluator "
                    "and question generator. "
                    "Always return valid JSON only. "
                    "Do not use markdown code fences."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={
            "type": "json_object"
        }
    )

    return response.choices[0].message.content


def ask_groq(prompt: str) -> str:
    """
    Use Groq API for free cloud deployment.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not configured."
        )

    # Groq uses the exact same OpenAI Python SDK
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key
    )

    response = client.chat.completions.create(
        model="llama3-8b-8192",  # Groq free model
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI interview evaluator "
                    "and question generator. "
                    "Always return valid JSON only. "
                    "Do not use markdown code fences."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={
            "type": "json_object"
        }
    )

    return response.choices[0].message.content