from typing import Any
from langchain_core.tools import tool
from ai.llm_adapter import generate_text_with_langchain


@tool
def leetcode_tool(topic: str = "arrays") -> dict[str, Any]:
    """
    Use this tool when the user asks for LeetCode problems,
    SQL LeetCode questions, coding practice problems,
    programming interview questions, or practice problems
    for SQL, Python, Java, arrays, strings, or algorithms.
    """

    try:
        prompt = f"""
Generate exactly 5 LeetCode-style practice problems for {topic}.

Return ONLY valid JSON in this exact structure:

[
  {{
    "number": "1",
    "title": "Problem title",
    "difficulty": "Easy",
    "problem": "Full problem statement",
    "input": "Input description",
    "output": "Output description",
    "example": {{
      "input": "Example input",
      "output": "Example output"
    }},
    "hint": "Short hint"
  }}
]

Rules:
- Generate exactly 5 problems.
- Do NOT return markdown.
- Do NOT return a paragraph.
- Do NOT return explanations outside the JSON.
- Include the complete problem statement.
- If topic is SQL, generate SQL/database problems.
- If topic is Python, generate Python problems.
- If topic is arrays, generate array problems.
"""

        answer = generate_text_with_langchain(
            prompt,
            system_prompt=(
                "You are an expert LeetCode coding interview coach. "
                "Return only valid JSON."
            )
        )

        import json

        # Remove accidental markdown code fences
        answer = answer.strip()

        if answer.startswith("```"):
            answer = answer.replace("```json", "").replace("```", "").strip()

        questions = json.loads(answer)

        return {
            "status": "success",
            "topic": topic,
            "questions": questions
        }

    except Exception as exc:
        return {
            "status": "error",
            "error": f"LeetCode guidance failed: {exc}"
        }