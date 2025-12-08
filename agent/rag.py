from typing import List, Optional

try:
    import chromadb
    from chromadb.utils import embedding_functions
except ImportError:
    chromadb = None
    embedding_functions = None

from config.settings import settings


def _create_collection():
    """
    Create or load a ChromaDB collection for our local vector store.
    Returns None if chromadb or embeddings are not available.
    """
    if chromadb is None or embedding_functions is None:
        return None
    if not settings.OPENAI_API_KEY:
        return None

    client = chromadb.PersistentClient(path=settings.VECTOR_PATH)
    embed_fn = embedding_functions.OpenAIEmbeddingFunction(
        api_key=settings.OPENAI_API_KEY,
        model_name="text-embedding-3-small",
    )
    collection = client.get_or_create_collection(
        name="sql_course_kb",
        embedding_function=embed_fn,
    )
    return collection


def _get_initial_docs() -> dict:
    """
    Knowledge base content for the agent (short and focused).
    """
    return {
        "sql_basics": (
            "Conceitos básicos de SQL: SELECT, FROM, WHERE, GROUP BY, ORDER BY, "
            "JOIN entre tabelas, chaves primárias e estrangeiras, filtros e agregações."
        ),
        "medallion": (
            "Arquitetura Medallion: Bronze (dados crus), Prata (dados tratados e padronizados), "
            "Ouro (dados agregados e modelados para análise de negócio)."
        ),
        "star_schema": (
            "Star Schema é um modelo dimensional com uma tabela fato central ligada a "
            "tabelas dimensão ao redor. Tabelas fato possuem métricas numéricas e chaves "
            "para dimensões como produto, tempo e campanha."
        ),
        "snowflake_schema": (
            "Snowflake Schema é uma variação do Star Schema em que dimensões são "
            "normalizadas em múltiplas tabelas, reduzindo redundância, mas aumentando "
            "a complexidade das consultas."
        ),
        "dim_fato": (
            "Tabelas dimensão armazenam contexto descritivo (produtos, clientes, campanhas). "
            "Tabelas fato armazenam métricas (vendas, cliques, impressões, gastos), "
            "geralmente com granularidade no tempo."
        ),
        "course_context": (
            "Cenário do curso: agência de marketing que gerencia campanhas de uma empresa "
            "de bebidas. Tabelas: dim_produto, dim_campanha e fato_marketing."
        ),
    }


def _ensure_loaded(collection) -> None:
    """Load initial documents into the collection if it's empty."""
    if collection is None:
        return
    if collection.count() > 0:
        return
    docs = _get_initial_docs()
    ids = list(docs.keys())
    documents = list(docs.values())
    collection.add(ids=ids, documents=documents)


def retrieve_docs(question: str, k: int = 4) -> List[str]:
    """
    Query the vector store for the most relevant documents.
    Returns an empty list if vector store is not available.
    """
    col = _create_collection()
    if col is None:
        return []
    _ensure_loaded(col)
    result = col.query(query_texts=[question], n_results=k)
    return result.get("documents", [[]])[0] or []
