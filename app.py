import streamlit as st

from db.connection import get_connection
from db.init_db import initialize_db

from ui.course import render_course_tab
from ui.sandbox import render_sandbox_tab
from ui.challenges import render_challenges_tab
from ui.progress import render_progress_tab
from ui.agent_chat import render_agent_tab

from utils.xp import _ensure_state  # opcional: forçar estado no começo


def main() -> None:
    st.set_page_config(
        page_title="Curso Interativo de SQL",
        layout="wide",
        page_icon="🧠",
    )

    # Initialize XP and other state
    _ensure_state()

    # Database connection
    conn = get_connection()
    initialize_db(conn)

    st.title("🎓 Curso Interativo de SQL")

    tab_curso, tab_sandbox, tab_desafios, tab_progresso, tab_agent = st.tabs(
        [
            "📘 Curso",
            "🧪 Sandbox SQL",
            "🎮 Desafios Gamificados",
            "🏅 Progresso",
            "🤖 Agente IA",
        ]
    )

    with tab_curso:
        render_course_tab()

    with tab_sandbox:
        render_sandbox_tab(conn)

    with tab_desafios:
        render_challenges_tab(conn)

    with tab_progresso:
        render_progress_tab()

    with tab_agent:
        render_agent_tab()


if __name__ == "__main__":
    main()
