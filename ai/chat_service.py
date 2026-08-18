import json
from langchain_core.messages import HumanMessage

from ai.agent import get_agent_executor, get_fallback_agent


class ChatService:

    def __init__(self, agent_executor=None):
        self.agent_executor = agent_executor or get_agent_executor()
        self.fallback_agent = get_fallback_agent()

    async def chat(self, message: str):

        try:
            result = await self.agent_executor.ainvoke({
                "messages": [
                    HumanMessage(content=message)
                ]
            })

            return self._extract_response(result)

        except Exception as primary_error:

            print(f"[PRIMARY AGENT FAILED] {primary_error}")

            # Try Groq fallback
            if self.fallback_agent is not None:

                try:
                    print("[FALLBACK] Switching to Groq...")

                    result = await self.fallback_agent.ainvoke({
                        "messages": [
                            HumanMessage(content=message)
                        ]
                    })

                    print("[FALLBACK] Groq succeeded")

                    return self._extract_response(result)

                except Exception as fallback_error:

                    print(f"[FALLBACK FAILED] {fallback_error}")

                    return (
                        f"Primary LLM failed: {primary_error}. "
                        f"Fallback LLM failed: {fallback_error}"
                    )

            return f"LangChain agent failed: {primary_error}"

    @staticmethod
    def _extract_response(result):

        if isinstance(result, dict):

            messages = result.get("messages") or []

            # Format structured leetcode_tool output as a readable string
            for msg in reversed(messages):
                tool_name = getattr(msg, "name", None)
                if tool_name == "leetcode_tool":
                    content = getattr(msg, "content", None)
                    parsed_data = None
                    if isinstance(content, str):
                        try:
                            parsed_data = json.loads(content)
                        except Exception:
                            pass
                    elif isinstance(content, dict):
                        parsed_data = content

                    if isinstance(parsed_data, dict) and parsed_data.get("status") == "success":
                        return ChatService._format_leetcode(parsed_data)
                    elif isinstance(parsed_data, dict) and parsed_data.get("status") == "error":
                        return parsed_data.get("error", "LeetCode tool encountered an error.")

            if "output" in result:
                return str(result["output"])

            if messages:

                last_message = messages[-1]

                content = getattr(
                    last_message,
                    "content",
                    None
                )

                if isinstance(content, list):

                    parts = []

                    for item in content:

                        if isinstance(item, dict):
                            parts.append(
                                str(item.get("text", ""))
                            )
                        else:
                            parts.append(str(item))

                    return "".join(parts).strip()

                if content:
                    return str(content).strip()

                return str(last_message)

        return str(result) if result is not None else ""

    @staticmethod
    def _format_leetcode(data: dict) -> str:
        """Convert a leetcode_tool success dict into a human-readable string."""
        topic = data.get("topic", "General")
        questions = data.get("questions", [])

        lines = [f"Here are 5 LeetCode-style {topic} practice problems:\n"]

        for q in questions:
            num = q.get("number", "?")
            title = q.get("title", "Untitled")
            diff = q.get("difficulty", "")
            problem = q.get("problem", "")
            inp = q.get("input", "")
            out = q.get("output", "")
            example = q.get("example", {})
            hint = q.get("hint", "")

            lines.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            lines.append(f"Problem {num}: {title}  [{diff}]\n")

            if problem:
                lines.append(f"{problem}\n")
            if inp:
                lines.append(f"Input:  {inp}")
            if out:
                lines.append(f"Output: {out}")
            if example:
                ex_in = example.get("input", "")
                ex_out = example.get("output", "")
                lines.append(f"\nExample:")
                if ex_in:
                    lines.append(f"  Input:  {ex_in}")
                if ex_out:
                    lines.append(f"  Output: {ex_out}")
            if hint:
                lines.append(f"\n💡 Hint: {hint}")
            lines.append("")

        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append("Good luck! Let me know if you want hints or solutions for any of these.")

        return "\n".join(lines)