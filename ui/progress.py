import streamlit as st

from utils.xp import get_xp, get_level, get_completed_challenges, get_total_challenges


def render_progress_tab() -> None:
    st.header("🏅 Progresso do Aluno")

    xp = get_xp()
    completed = get_completed_challenges()
    level = get_level(xp)
    total_challenges = get_total_challenges()

    col1, col2, col3 = st.columns(3)
    col1.metric("XP total", xp)
    col2.metric("Desafios concluídos", f"{len(completed)} / {total_challenges}")
    col3.metric("Nível atual", level)

    st.markdown("### ✅ Desafios concluídos")

    if completed:
        for cid in sorted(list(completed)):
            st.write(f"- Desafio {cid}")
    else:
        st.write("Você ainda não concluiu nenhum desafio. Vá na aba **Desafios Gamificados** para começar.")

    st.markdown("---")
    st.markdown("### Próximos passos sugeridos")
    st.write(
        "- Finalizar todos os desafios\n"
        "- Criar suas próprias perguntas de negócio e escrever queries\n"
        "- Explorar a aba de Sandbox para testar ideias"
    )
