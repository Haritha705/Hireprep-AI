import json
import re
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
Generate 3 high-yield LeetCode-style practice problems for topic: {topic}.

Return ONLY a valid JSON array matching this exact schema:
[
  {{
    "number": "1",
    "title": "Problem Title",
    "difficulty": "Easy",
    "problem": "Clear problem statement",
    "input": "Input description",
    "output": "Output description",
    "example": {{
      "input": "Example input",
      "output": "Example output"
    }},
    "hint": "Helpful hint"
  }}
]

Rules:
- Output valid JSON only, no surrounding conversational text.
- If topic is SQL, generate practical SQL query challenges.
- If topic is Python, generate Python data structure/algorithm challenges.
"""

        answer = generate_text_with_langchain(
            prompt,
            system_prompt="You are an expert LeetCode interview coach. Return only the JSON array."
        )

        # Robust extraction: find the JSON array inside the LLM answer
        match = re.search(r'\[\s*\{.*\}\s*\]', answer, re.DOTALL)
        if match:
            json_str = match.group(0)
            questions = json.loads(json_str)
        else:
            # Fallback cleaning if standard fences used
            cleaned = answer.replace("```json", "").replace("```", "").strip()
            questions = json.loads(cleaned)

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