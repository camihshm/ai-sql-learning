import streamlit as st
import sqlite3

from db.queries import run_query


def render_sandbox_tab(conn: sqlite3.Connection) -> None:
    st.header("🧪 Sandbox SQL")
    st.write("Digite qualquer comando `SELECT` para explorar o banco de dados.")

    col1, col2 = st.columns([2, 1])

    with col1:
        default_query = "SELECT * FROM dim_produto;"
        user_query = st.text_area(
            "Sua query SQL:",
            value=default_query,
            height=150,
            key="sandbox_query",
        )

        if st.button("Executar consulta", type="primary"):
            try:
                df = run_query(conn, user_query)
                st.success(f"Consulta executada com sucesso! {len(df)} linha(s) retornadas.")
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao executar a query:\n\n{e}")

    with col2:
        st.markdown("### 🧮 Dicas rápidas")
        st.markdown("- `SELECT * FROM dim_produto;`")
        st.markdown("- `SELECT * FROM dim_campanha;`")
        st.markdown("- `SELECT * FROM fato_marketing;`")
        st.markdown("- Use `WHERE` para filtrar (`WHERE canal = 'Instagram'`).")
        st.markdown("- Use `GROUP BY` para agrupar (`GROUP BY canal`).")
