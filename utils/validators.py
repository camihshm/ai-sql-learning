from dataclasses import dataclass
from typing import Optional

import pandas as pd
import sqlite3

from db.queries import run_query


@dataclass
class ValidationResult:
    ok: bool
    error: Optional[str]
    df_user: Optional[pd.DataFrame]
    df_expected: Optional[pd.DataFrame]


def _normalize_df(df: pd.DataFrame | None) -> pd.DataFrame | None:
    """
    Sort rows and columns so that DataFrames become comparable
    regardless of ordering.
    """
    if df is None or df.empty:
        return df
    norm = df.copy()
    norm = norm.reindex(sorted(norm.columns), axis=1)
    norm = norm.sort_values(by=list(norm.columns)).reset_index(drop=True)
    return norm


def validate_answer(
    conn: sqlite3.Connection,
    expected_query: str,
    user_query: str,
) -> ValidationResult:
    """
    Compare the result of user_query with expected_query.
    """

    try:
        df_expected = run_query(conn, expected_query)
    except Exception as e:
        # Se der erro aqui, é problema no gabarito
        return ValidationResult(
            ok=False,
            error=f"Erro ao executar query esperada (gabarito): {e}",
            df_user=None,
            df_expected=None,
        )

    try:
        df_user = run_query(conn, user_query)
    except Exception as e:
        return ValidationResult(
            ok=False,
            error=str(e),
            df_user=None,
            df_expected=df_expected,
        )

    df_expected_norm = _normalize_df(df_expected)
    df_user_norm = _normalize_df(df_user)

    ok = df_expected_norm.equals(df_user_norm)

    return ValidationResult(
        ok=ok,
        error=None,
        df_user=df_user,
        df_expected=df_expected,
    )
