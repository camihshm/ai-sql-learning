import streamlit as st
import pandas as pd
import sqlite3

from agent.agent import answer_question
from db.connection import get_connection
from db.queries import run_query


# -----------------------
# 🔒 Lista de temas proibidos
# -----------------------
FORBIDDEN_TOPICS = [
    "ignore", "jailbreak", "prompt", "regras", "system prompt",
    "prisão", "hacker", "hackear", "burlar", "bypass", "desobedecer",
    "modificar instruções", "exploit", "conteúdo adulto", "política",
    "religião", "violência"
]


def is_forbidden(message: str) -> bool:
    """Detecta tentativas de jailbreak ou assuntos proibidos."""
    msg = message.lower()
    return any(word in msg for word in FORBIDDEN_TOPICS)


# ------------------------------------------------------------
# 🎨 Renderização do layout e comportamento do agente
# ------------------------------------------------------------
def render_agent_tab():

    st.header("🤖 Agente IA — Assistente Oficial do Curso de SQL & Arquitetura de Dados")

    st.markdown(
        """
### 📌 O que o agente pode responder
O agente está autorizado **somente** a responder sobre:

- SQL (DDL, DML, SELECT, JOIN, GROUP BY, etc.)
- Arquitetura de Dados (Medallion, Star Schema, Snowflake)
- Modelagem Dimensional (tabelas fato e dimensão)
- Correção e análise de queries SQL
- Execução de comandos SQL no SQLite do curso

💡 *Perguntas fora desse escopo são bloqueadas automaticamente.*
        """
    )

    st.divider()

    # --------------------------------------------
    # Inicializa o histórico
    # --------------------------------------------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # --------------------------------------------
    # Botão de nova conversa
    # --------------------------------------------
    if st.button("🧹 Nova conversa"):
        st.session_state.chat_history = []
        st.success("Conversa reiniciada!")
        st.experimental_rerun()

    st.subheader("💬 Chat com o Agente")

    # --------------------------------------------
    # Apresentação do histórico do chat
    # --------------------------------------------
    for sender, text in st.session_state.chat_history:
        if sender == "user":
            avatar = "🧑‍💻"
            bubble_color = "#DCF8C6"
            align = "right"
            margin_side = "auto"
        else:
            avatar = "🤖"
            bubble_color = "#F1F0F0"
            align = "left"
            margin_side = "0"

        st.markdown(
            f"""
            <div style="
                background-color:{bubble_color};
                padding:12px;
                border-radius:12px;
                max-width:70%;
                margin-bottom:10px;
                text-align:{align};
                margin-left:{margin_side};
            ">
                <strong>{avatar} {sender.capitalize()}:</strong><br>
                {text}
            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------
    # Campo de entrada do usuário
    # --------------------------------------------
    user_message = st.text_input("Digite sua pergunta:", key="chat_input")

    # --------------------------------------------
    # Upload opcional de arquivo SQL
    # --------------------------------------------
    uploaded_file = st.file_uploader("Envie um arquivo .sql para análise opcional", type=["sql"])

    conn = get_connection()

    if st.button("Enviar", type="primary"):

        # Caso o aluno tenha enviado um arquivo .sql
        if uploaded_file is not None:
            sql_query = uploaded_file.read().decode("utf-8")

            st.markdown("### 📄 Conteúdo do arquivo .sql enviado:")
            st.code(sql_query, language="sql")

            try:
                df = run_query(conn, sql_query)
                st.success("Query executada com sucesso!")
                st.dataframe(df)
            except Exception as e:
                st.error(f"Erro ao executar SQL do arquivo: {e}")

        # Caso esteja digitando no chat
        if user_message.strip():

            # 🔒 Verifica se o conteúdo é permitido
            if is_forbidden(user_message):
                bot_reply = (
                    "Desculpe, mas não posso responder perguntas ou comandos fora do assunto permitido. "
                    "Vamos focar em SQL, arquitetura de dados e modelagem dimensional 😊"
                )
                st.session_state.chat_history.append(("user", user_message))
                st.session_state.chat_history.append(("agent", bot_reply))
                st.experimental_rerun()

            # Se for SQL, tenta executar
            if user_message.lower().startswith(("select", "with", "pragma")):
                try:
                    df = run_query(conn, user_message)
                    st.success("Query executada com sucesso!")
                    st.dataframe(df)
                except Exception as e:
                    st.error(f"Erro na query SQL:\n{e}")

            # Gera resposta do agente
            with st.spinner("O agente está pensando..."):
                bot_response = answer_question(user_message)

            # Salva histórico da conversa
            st.session_state.chat_history.append(("user", user_message))
            st.session_state.chat_history.append(("agent", bot_response))

            st.experimental_rerun()
