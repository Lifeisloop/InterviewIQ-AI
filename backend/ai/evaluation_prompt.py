def build_evaluation_prompt(
    question: str,
    candidate_answer: str
) -> str:
    """
    Build a strict prompt for evaluating one interview answer.
    """

    return f"""
You are a strict, fair, and accurate technical interview evaluator.

Evaluate the candidate's answer using only:
1. The interview question
2. The candidate's actual answer

INTERVIEW QUESTION:
{question}

CANDIDATE ANSWER:
{candidate_answer}

EVALUATION RULES:

1. Give an integer score from 0 to 10.

2. The score must reflect:
   - technical correctness
   - relevance
   - completeness
   - clarity
   - practical understanding

3. "strengths" must contain ONLY genuine positive points
   that are clearly supported by the candidate's answer.

4. Every strength must be specific.

5. Explain exactly what the candidate got correct.

6. NEVER place negative feedback inside "strengths".

7. Do not use vague strengths such as:
   - "Directly answers the question"
   - "Technically accurate"
   - "Good answer"
   - "Relevant answer"
   - "Correct answer"

8. Good strength examples:
   - "Correctly identifies Pandas as a library for data manipulation"
   - "Recognizes that SQL JOINs combine related data from multiple tables"
   - "Correctly identifies Power BI as a dashboard and visualization tool"

9. "weaknesses" must contain ONLY:
   - incorrect statements
   - missing concepts
   - lack of depth
   - vague explanations
   - missing examples
   - incomplete technical details

10. NEVER place positive feedback inside "weaknesses".

11. If there is no genuine strength, return:
    "strengths": []

12. If there is no genuine weakness, return:
    "weaknesses": []

13. Do not invent:
    - experience
    - projects
    - skills
    - tools
    - knowledge
    - examples
    that the candidate did not mention.

14. Avoid duplicate or near-duplicate feedback.

15. Use correct spelling and professional grammar.

16. Keep every strength concise and specific.

17. Keep every weakness concise and specific.

18. The ideal answer must:
    - directly answer the question
    - be technically accurate
    - be concise but complete
    - improve on the candidate's answer
    - avoid unnecessary information

19. Do not unfairly reward a vague answer.

20. Do not unfairly punish a correct concise answer.

21. Return ONLY valid JSON.

22. Do not use markdown.

23. Do not use ```json code fences.

24. Do not include any explanation outside the JSON.

Return exactly this JSON structure:

{{
  "score": 0,
  "strengths": [
    "Specific positive point"
  ],
  "weaknesses": [
    "Specific missing or incorrect point"
  ],
  "ideal_answer": "A technically accurate improved answer"
}}
"""