"""Predicciones guardadas de cada variante, para combinarlas y enviarlas sin reentrenar.

Al terminar una variante:

    res = validacion_cruzada(fit_predict, train, nombre="tfidf_ridge")
    preds_test = fit_predict(train, test)              # entrenando con todo train
    guardar_predicciones("tfidf_ridge", train, res["oof"], test, preds_test)

Escribe predicciones/tfidf_ridge_oof.csv (1.288 usuarios de train, validación cruzada)
y predicciones/tfidf_ridge_test.csv (323 usuarios de test). Son pequeños y se suben a git.
"""

from __future__ import annotations

import re

import numpy as np
import pandas as pd

from src.config import PREDICCIONES_DIR, TRAITS


def _a_csv(df_usuarios: pd.DataFrame, preds: np.ndarray, ruta) -> None:
    preds = np.asarray(preds, dtype=float)
    if preds.shape != (len(df_usuarios), len(TRAITS)):
        raise ValueError(f"Forma {preds.shape}, se esperaba {(len(df_usuarios), len(TRAITS))}")
    if np.isnan(preds).any():
        raise ValueError("Hay predicciones vacías (NaN)")
    out = pd.DataFrame(np.clip(preds, 0, 100), columns=TRAITS)
    out.insert(0, "username", df_usuarios["username"].to_numpy())
    out.to_csv(ruta, index=False, float_format="%.4f")


def guardar_predicciones(nombre: str, train_df: pd.DataFrame, oof: np.ndarray,
                         test_df: pd.DataFrame, preds_test: np.ndarray) -> None:
    """Guarda las predicciones OOF (train) y de test de una variante."""
    if not re.fullmatch(r"[A-Za-z0-9-]+(_[A-Za-z0-9-]+)*", nombre):
        raise ValueError("El nombre solo puede tener letras, números, '-' y '_'")
    PREDICCIONES_DIR.mkdir(exist_ok=True)
    _a_csv(train_df, oof, PREDICCIONES_DIR / f"{nombre}_oof.csv")
    _a_csv(test_df, preds_test, PREDICCIONES_DIR / f"{nombre}_test.csv")
    print(f"Predicciones guardadas: predicciones/{nombre}_oof.csv y _test.csv")


def cargar_predicciones(nombre: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(oof, test) de una variante, indexados por username con columnas TRAITS."""
    oof = pd.read_csv(PREDICCIONES_DIR / f"{nombre}_oof.csv", keep_default_na=False).set_index("username")
    test = pd.read_csv(PREDICCIONES_DIR / f"{nombre}_test.csv", keep_default_na=False).set_index("username")
    return oof[TRAITS], test[TRAITS]


def listar_variantes() -> list[str]:
    """Variantes que tienen predicciones OOF y de test guardadas."""
    oof = {p.name[: -len("_oof.csv")] for p in PREDICCIONES_DIR.glob("*_oof.csv")}
    test = {p.name[: -len("_test.csv")] for p in PREDICCIONES_DIR.glob("*_test.csv")}
    return sorted(oof & test)
