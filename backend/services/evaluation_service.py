import json
import re

from ai.evaluation_prompt import build_evaluation_prompt
from ai.llm import ask_llm


NEGATIVE_PHRASES = [
    "lack",
    "lacks",
    "lacking",
    "missing",
    "incorrect",
    "incorrectly",
    "fails",
    "failed",
    "failure",
    "does not",
    "doesn't",
    "did not",
    "didn't",
    "limited",
    "unclear",
    "incomplete",
    "insufficient",
    "too vague",
    "vague",
    "no example",
    "no examples",
    "wrong",
    "not clear",
    "not enough",
    "doesn't provide",
    "does not provide",
    "not fully",
    "needs more",
]


VAGUE_STRENGTHS = [
    "directly answers the question",
    "answers the question",
    "technically accurate",
    "is technically accurate",
    "is technially accurate",
    "good answer",
    "relevant answer",
    "correct answer",
]


def is_negative_feedback(text: str) -> bool:
    """
    Detect obviously negative feedback that was incorrectly
    placed inside the strengths list.
    """

    normalized_text = text.strip().lower()

    return any(
        phrase in normalized_text
        for phrase in NEGATIVE_PHRASES
    )


def is_vague_strength(text: str) -> bool:
    """
    Remove generic strengths that provide no useful feedback.
    """

    normalized_text = text.strip().lower()

    return any(
        normalized_text == phrase
        for phrase in VAGUE_STRENGTHS
    )


def normalize_feedback_text(text: str) -> str:
    """
    Clean extra spaces and normalize feedback text.
    """

    if not isinstance(text, str):
        return ""

    cleaned = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return cleaned


def remove_duplicates(items: list) -> list:
    """
    Remove case-insensitive duplicate feedback items
    while preserving original order.
    """

    seen = set()
    unique_items = []

    for item in items:
        cleaned = normalize_feedback_text(item)

        if not cleaned:
            continue

        key = cleaned.lower()

        if key not in seen:
            seen.add(key)
            unique_items.append(cleaned)

    return unique_items


def normalize_score(score) -> int:
    """
    Convert score safely to an integer between 0 and 10.
    """

    try:
        numeric_score = float(score)

        numeric_score = max(
            0,
            min(10, numeric_score)
        )

        return round(numeric_score)

    except (TypeError, ValueError):
        return 0


def extract_json_response(response: str) -> dict:
    """
    Parse JSON safely.

    Also handles accidental Markdown code fences
    returned by the LLM.
    """

    if not isinstance(response, str):
        raise ValueError(
            "LLM response must be a string."
        )

    cleaned_response = response.strip()

    if cleaned_response.startswith("```"):
        cleaned_response = re.sub(
            r"^```(?:json)?\s*",
            "",
            cleaned_response,
            flags=re.IGNORECASE
        )

        cleaned_response = re.sub(
            r"\s*```$",
            "",
            cleaned_response
        )

    return json.loads(cleaned_response)


def clean_evaluation_result(result: dict) -> dict:
    """
    Validate and clean the LLM evaluation result.
    """

    raw_strengths = result.get(
        "strengths",
        []
    )

    raw_weaknesses = result.get(
        "weaknesses",
        []
    )

    if not isinstance(raw_strengths, list):
        raw_strengths = []

    if not isinstance(raw_weaknesses, list):
        raw_weaknesses = []

    clean_strengths = []

    clean_weaknesses = [
        normalize_feedback_text(item)
        for item in raw_weaknesses
        if isinstance(item, str)
    ]

    for strength in raw_strengths:

        if not isinstance(strength, str):
            continue

        cleaned_strength = normalize_feedback_text(
            strength
        )

        if not cleaned_strength:
            continue

        if is_negative_feedback(cleaned_strength):
            clean_weaknesses.append(
                cleaned_strength
            )

        elif is_vague_strength(cleaned_strength):
            continue

        else:
            clean_strengths.append(
                cleaned_strength
            )

    clean_strengths = remove_duplicates(
        clean_strengths
    )

    clean_weaknesses = remove_duplicates(
        clean_weaknesses
    )

    ideal_answer = result.get(
        "ideal_answer",
        ""
    )

    if not isinstance(ideal_answer, str):
        ideal_answer = str(ideal_answer)

    return {
        "score": normalize_score(
            result.get("score", 0)
        ),
        "strengths": clean_strengths,
        "weaknesses": clean_weaknesses,
        "ideal_answer": ideal_answer.strip()
    }


def evaluate_answer(data):
    """
    Evaluate one candidate answer using the LLM.
    """

    prompt = build_evaluation_prompt(
        question=data.question,
        candidate_answer=data.candidate_answer
    )

    response = ask_llm(prompt)

    print("\nRAW EVALUATION RESPONSE:")
    print(response)

    try:
        result = extract_json_response(
            response
        )

        return clean_evaluation_result(
            result
        )

    except (
        json.JSONDecodeError,
        ValueError,
        TypeError
    ) as error:

        print(
            "EVALUATION PARSE ERROR:",
            error
        )

        return {
            "score": 0,
            "strengths": [],
            "weaknesses": [
                "The AI evaluation response could not be processed."
            ],
            "ideal_answer": "",
            "error": str(error)
        }


def evaluate_candidate_answer(
    question: str,
    candidate_answer: str
):
    """
    Compatibility function used by report_service.py.
    """

    class EvaluationData:
        def __init__(
            self,
            question: str,
            candidate_answer: str
        ):
            self.question = question
            self.candidate_answer = candidate_answer

    data = EvaluationData(
        question=question,
        candidate_answer=candidate_answer
    )

    return evaluate_answer(data)