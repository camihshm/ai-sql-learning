import streamlit as st


def _ensure_state() -> None:
    """
    Ensure XP and challenge state are in session_state.
    """
    if "xp" not in st.session_state:
        st.session_state["xp"] = 0
    if "completed_challenges" not in st.session_state:
        st.session_state["completed_challenges"] = set()
    if "total_challenges" not in st.session_state:
        # Pode ser atualizado pela UI de desafios, se quiser algo dinâmico.
        st.session_state["total_challenges"] = 3


def add_xp(challenge_id: int, xp_gain: int = 20) -> None:
    """
    Add XP once per challenge.
    """
    _ensure_state()
    completed = st.session_state["completed_challenges"]
    if challenge_id not in completed:
        completed.add(challenge_id)
        st.session_state["completed_challenges"] = completed
        st.session_state["xp"] += xp_gain


def get_xp() -> int:
    _ensure_state()
    return int(st.session_state["xp"])


def get_completed_challenges() -> set:
    _ensure_state()
    return st.session_state["completed_challenges"]


def get_total_challenges() -> int:
    _ensure_state()
    return int(st.session_state["total_challenges"])


def get_level(xp: int) -> str:
    """
    Simple level logic based on XP.
    """
    if xp < 60:
        return "Estagiário SQL"
    if xp < 120:
        return "Analista Júnior SQL"
    if xp < 180:
        return "Analista Pleno SQL"
    if xp < 220:
        return "Especialista SQL em Marketing"
    return "Consultor SQL Marketing Jedi"
