"""Evaluación común: TODAS las variantes se miden con esta validación cruzada.

Contrato de una variante: una función

    fit_predict(train_df, val_df) -> np.ndarray de forma (len(val_df), 5)

train_df y val_df son filas de authors_train (username + 5 rasgos, con NaN
posibles). La función entrena solo con train_df (texto, vocabulario, escalado,
todo) y predice val_df en el orden de TRAITS. Ajustar algo con val_df o con
todos los usuarios a la vez es fuga de datos y hace trampas al RMSE.
"""

from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, clone
from sklearn.model_selection import KFold

from src.config import N_FOLDS, SEED, TRAITS


def folds(train_df: pd.DataFrame) -> list[tuple[np.ndarray, np.ndarray]]:
    """Índices (train, val) de los N_FOLDS folds fijos."""
    kf = KFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
    return list(kf.split(train_df))


def rmse_por_rasgo(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """RMSE de cada rasgo ignorando las etiquetas que faltan (NaN)."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    err = np.where(np.isnan(y_true), np.nan, (y_true - y_pred) ** 2)
    return np.sqrt(np.nanmean(err, axis=0))


def validacion_cruzada(
    fit_predict: Callable[[pd.DataFrame, pd.DataFrame], np.ndarray],
    train_df: pd.DataFrame,
    nombre: str = "variante",
) -> dict:
    """Ejecuta los folds y devuelve RMSE por rasgo, RMSE medio y predicciones OOF."""
    oof = np.full((len(train_df), len(TRAITS)), np.nan)
    por_fold = []
    for i, (tr, va) in enumerate(folds(train_df)):
        pred = np.clip(np.asarray(fit_predict(train_df.iloc[tr], train_df.iloc[va]), dtype=float), 0, 100)
        if pred.shape != (len(va), len(TRAITS)):
            raise ValueError(f"fit_predict debe devolver forma {(len(va), len(TRAITS))}, devolvió {pred.shape}")
        oof[va] = pred
        por_fold.append(rmse_por_rasgo(train_df.iloc[va][TRAITS].to_numpy(), pred).mean())

    rasgos = rmse_por_rasgo(train_df[TRAITS].to_numpy(), oof)
    res = {
        "nombre": nombre,
        "rmse_rasgos": dict(zip(TRAITS, rasgos.round(3))),
        "rmse_medio": round(float(rasgos.mean()), 3),
        "rmse_folds": [round(float(x), 3) for x in por_fold],
        "oof": oof,
    }
    imprimir(res)
    return res


def imprimir(res: dict) -> None:
    """Línea lista para copiar a EXPERIMENTOS.md."""
    r = res["rmse_rasgos"]
    print(f"{res['nombre']}: RMSE medio {res['rmse_medio']:.3f} (folds {res['rmse_folds']})")
    print("| " + " | ".join(TRAITS) + " | medio |")
    print("| " + " | ".join(f"{r[t]:.2f}" for t in TRAITS) + f" | **{res['rmse_medio']:.2f}** |")


class PorRasgo:
    """Entrena un clon del estimador por rasgo, saltándose las filas con NaN.

    Ejemplo: PorRasgo(Ridge(alpha=10)).fit(X_tr, y_tr).predict(X_va)
    """

    def __init__(self, estimador: BaseEstimator):
        self.estimador = estimador

    def fit(self, X, y):
        y = np.asarray(y, dtype=float)
        self.modelos_ = []
        for j in range(y.shape[1]):
            ok = ~np.isnan(y[:, j])
            self.modelos_.append(clone(self.estimador).fit(X[ok], y[ok, j]))
        return self

    def predict(self, X) -> np.ndarray:
        return np.column_stack([m.predict(X) for m in self.modelos_])
