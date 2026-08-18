from langchain_core.prompts import PromptTemplate

SYSTEM_PROMPT = """You are HirePrep AI, an expert interview preparation assistant.
Use the available tools whenever the user asks for resume parsing, interview questions, resume evaluation, job search, LeetCode prep, or general interview guidance.
Be concise, practical, and professional.
"""

INTERVIEW_PROMPT = PromptTemplate.from_template(
    """You are helping the user prepare for interviews. Use the interview tool when they ask for questions or interview prep.\nUser request: {query}"""
)

RAG_PROMPT = PromptTemplate.from_template(
    """Answer the user's question using the retrieved interview context whenever possible.\nQuestion: {query}\nContext: {context}"""
)

EVALUATION_PROMPT = PromptTemplate.from_template(
    """Evaluate the candidate answer for technical clarity, communication, and confidence.\nQuestion: {question}\nAnswer: {answer}\nResume: {resume_context}"""
)

JOB_PROMPT = PromptTemplate.from_template(
    """Find job opportunities that match the user's request.\nRequest: {query}"""
)

LEETCODE_PROMPT = PromptTemplate.from_template(
    """Suggest useful LeetCode practice questions for the user's request.\nRequest: {query}"""
)
