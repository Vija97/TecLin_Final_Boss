"""Generar y validar ficheros de entrega.

    from src.submission import generar_entrega
    generar_entrega(test_df, preds, "tfidf_ridge")   # -> submissions/<equipo>_tfidf_ridge.csv

Para comprobar un CSV ya hecho:

    python -m src.submission submissions/<equipo>_<variante>.csv
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import SUBMISSIONS_DIR, TEAM_NAME, TEST_CSV, TRAITS

COLUMNAS = ["team_name", "variant_name", "username", *TRAITS]


def generar_entrega(test_df: pd.DataFrame, preds: np.ndarray, variante: str) -> Path:
    """Escribe el CSV con el formato del enunciado y lo valida."""
    if not re.fullmatch(r"[A-Za-z0-9-]+(_[A-Za-z0-9-]+)*", variante):
        raise ValueError("El nombre de la variante solo puede tener letras, números, '-' y '_'")
    preds = np.clip(np.asarray(preds, dtype=float), 0, 100)
    df = pd.DataFrame(preds, columns=TRAITS)
    df.insert(0, "username", test_df["username"].to_numpy())
    df.insert(0, "variant_name", variante)
    df.insert(0, "team_name", TEAM_NAME)

    SUBMISSIONS_DIR.mkdir(exist_ok=True)
    ruta = SUBMISSIONS_DIR / f"{TEAM_NAME}_{variante}.csv"
    df.to_csv(ruta, index=False)
    validar_entrega(ruta)
    return ruta


def validar_entrega(ruta: str | Path) -> None:
    """Lanza AssertionError con el motivo si el fichero no es entregable."""
    ruta = Path(ruta)
    df = pd.read_csv(ruta)
    esperados = set(pd.read_csv(TEST_CSV)["username"])

    assert list(df.columns) == COLUMNAS, f"Columnas {list(df.columns)} != {COLUMNAS}"
    assert df["team_name"].nunique() == 1 and df["team_name"].iloc[0] == TEAM_NAME, "team_name incorrecto"
    assert df["variant_name"].nunique() == 1, "Debe haber un único variant_name"
    variante = df["variant_name"].iloc[0]
    assert ruta.name == f"{TEAM_NAME}_{variante}.csv", f"El fichero debería llamarse {TEAM_NAME}_{variante}.csv"
    assert not df["username"].duplicated().any(), "Hay usuarios repetidos"
    faltan, sobran = esperados - set(df["username"]), set(df["username"]) - esperados
    assert not faltan and not sobran, f"Faltan {len(faltan)} usuarios y sobran {len(sobran)}"
    assert not df[TRAITS].isna().any().any(), "Hay predicciones vacías"
    assert df[TRAITS].ge(0).all().all() and df[TRAITS].le(100).all().all(), "Hay valores fuera de [0, 100]"
    print(f"OK: {ruta.name} ({len(df)} usuarios)")


if __name__ == "__main__":
    for r in sys.argv[1:]:
        validar_entrega(r)
