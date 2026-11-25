"""Tipo MBTI de cada usuario extraído de su propio texto (#22, #32). No usa etiquetas.

    from src.mbti import extraer_tipos, features_mbti
    tipo_auto, tipo_menc = extraer_tipos(cargar_posts())
    F = features_mbti(train["username"], tipo_auto, tipo_menc, con_menciones=True)   # (n, 5)
"""

from __future__ import annotations

import numpy as np
import pandas as pd

AUTO = r"(?i)\b(?:i'?m|i am|as an?|me,? an?)\s+(?:an?\s+)?([ie][ns][tf][jp])\b"
TIPO = r"(?<![A-Za-z])([IEie][NSns][TFtf][JPjp])(?![A-Za-z])"
MIN_MENCIONES = 3


def _mas_frecuente(s: pd.Series) -> str:
    return s.value_counts().index[0]


def extraer_tipos(posts: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """(tipo autoidentificado, tipo más mencionado con ≥ MIN_MENCIONES), indexados por username."""
    a = posts["body"].str.extract(AUTO)[0].dropna()
    tipo_auto = (pd.Series(a.str.upper().to_numpy(), index=posts["username"].to_numpy()[a.index])
                 .groupby(level=0).agg(_mas_frecuente))
    m = posts["body"].str.extractall(TIPO)
    menc = pd.Series(m[0].str.upper().to_numpy(), index=posts["username"].to_numpy()[m.index.get_level_values(0)])
    n = menc.groupby(level=0).size()
    tipo_menc = menc.groupby(level=0).agg(_mas_frecuente)[n >= MIN_MENCIONES]
    return tipo_auto, tipo_menc


def features_mbti(usuarios, tipo_auto: pd.Series, tipo_menc: pd.Series | None = None,
                  con_menciones: bool = False) -> np.ndarray:
    """5 columnas: E/I, N/S, F/T, J/P como +1/−1 (0 sin tipo) y un indicador de "tiene tipo"."""
    t = pd.Series(np.asarray(usuarios)).map(tipo_auto)
    if con_menciones and tipo_menc is not None:
        t = t.fillna(pd.Series(np.asarray(usuarios)).map(tipo_menc))
    F = np.zeros((len(t), 5))
    for i, x in enumerate(t):
        if isinstance(x, str):
            F[i] = [1 if x[0] == "E" else -1, 1 if x[1] == "N" else -1,
                    1 if x[2] == "F" else -1, 1 if x[3] == "J" else -1, 1]
    return F
