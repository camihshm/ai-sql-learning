from typing import Dict, Any, List

import streamlit as st
import sqlite3

from utils.validators import validate_answer
from utils.xp import add_xp


def _get_challenges() -> List[Dict[str, Any]]:
    """
    Returns the list of challenges and their expected queries.
    """
    return [
        {
            "id": 1,
            "titulo": "Vendas por produto",
            "descricao": "Liste o total de vendas por produto.",
            "dica": "Use SUM(vendas) e GROUP BY nome_produto.",
            "expected_query": """
                SELECT p.nome_produto, SUM(f.vendas) AS total_vendas
                FROM fato_marketing f
                JOIN dim_produto p ON f.id_produto = p.id_produto
                GROUP BY p.nome_produto
            """,
        },
        {
            "id": 2,
            "titulo": "Gasto total por canal",
            "descricao": "Calcule quanto foi gasto em cada canal de campanha.",
            "dica": "Use SUM(gastos) e agrupe por canal.",
            "expected_query": """
                SELECT c.canal, SUM(f.gastos) AS total_gasto
                FROM fato_marketing f
                JOIN dim_campanha c ON f.id_campanha = c.id_campanha
                GROUP BY c.canal
            """,
        },
        {
            "id": 3,
            "titulo": "Maior número de cliques por canal",
            "descricao": "Mostre o maior número de cliques registrado por canal.",
            "dica": "Use MAX(cliques) e GROUP BY canal.",
            "expected_query": """
                SELECT c.canal, MAX(f.cliques) AS max_cliques
                FROM fato_marketing f
                JOIN dim_campanha c ON f.id_campanha = c.id_campanha
                GROUP BY c.canal
            """,
        },
    ]


def render_challenges_tab(conn: sqlite3.Connection) -> None:
    st.header("🎮 Desafios Gamificados")
    st.write(
        "Responda aos desafios escrevendo queries SQL. "
        "Se o resultado bater com o esperado, você ganha XP!"
    )

    challenges = _get_challenges()
    options = {f"{c['id']} - {c['titulo']}": c for c in challenges}

    selected_label = st.selectbox("Escolha um desafio:", list(options.keys()))
    challenge = options[selected_label]

    st.subheader(f"Desafio {challenge['id']} – {challenge['titulo']}")
    st.write(challenge["descricao"])

    with st.expander("💡 Dica"):
        st.write(challenge["dica"])

    user_sql = st.text_area(
        "Digite sua query de resposta:",
        height=150,
        key=f"challenge_sql_{challenge['id']}",
    )

    if st.button("Validar resposta", type="primary", key=f"validate_{challenge['id']}"):
        if not user_sql.strip():
            st.warning("Digite uma query antes de validar.")
            return

        result = validate_answer(conn, challenge["expected_query"], user_sql)

        if result.error:
            st.error(f"Erro na execução da sua query:\n\n{result.error}")
        elif result.ok:
            st.success("🎉 Correto! Sua resposta gera o mesmo resultado que a solução esperada. +20 XP")
            add_xp(challenge_id=challenge["id"], xp_gain=20)
        else:
            st.warning(
                "A query executou, mas o resultado é diferente do esperado. "
                "Compare abaixo e ajuste sua resposta."
            )
            if result.df_user is not None:
                st.markdown("#### 🔎 Seu resultado")
                st.dataframe(result.df_user, use_container_width=True)
            if result.df_expected is not None:
                st.markdown("#### ✅ Resultado esperado")
                st.dataframe(result.df_expected, use_container_width=True)
