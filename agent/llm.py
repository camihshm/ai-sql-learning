from typing import List

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # type: ignore

from config.settings import settings


def generate_answer(system_prompt: str, user_message: str, context_docs: List[str]) -> str:
    """
    Call OpenAI Chat API with a structured prompt.
    If OpenAI or API key is not available, returns a fallback message.
    """
    if OpenAI is None or not settings.OPENAI_API_KEY:
        context_text = "\n\n".join(context_docs) if context_docs else "(sem contexto)"
        return (
            "O agente IA não está configurado (OPENAI_API_KEY ausente ou dependências faltando).\n\n"
            "Pergunta do aluno:\n"
            f"{user_message}\n\n"
            "Contexto disponível:\n"
            f"{context_text}"
        )

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    context_block = ""
    if context_docs:
        joined_docs = "\n\n---\n\n".join(context_docs)
        context_block = f"Use as informações abaixo como contexto adicional:\n{joined_docs}"

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"{context_block}\n\nPergunta do aluno:\n{user_message}",
        },
    ]

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.2,
    )
    return completion.choices[0].message.content
