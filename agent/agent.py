from typing import List

from agent.prompts import SYSTEM_PROMPT
from agent.rag import retrieve_docs
from agent.llm import generate_answer


def answer_question(question: str) -> str:
    """
    Full RAG pipeline:
    1. Retrieve relevant chunks
    2. Call LLM with system prompt + context
    """
    context_docs: List[str] = retrieve_docs(question, k=4)
    answer = generate_answer(SYSTEM_PROMPT, question, context_docs)
    return answer
