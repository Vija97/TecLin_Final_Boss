"""Carga de autores y posts.

Uso típico:

    from src.data import cargar_autores, textos_por_usuario
    train, test = cargar_autores()
    textos = textos_por_usuario()          # Series username -> texto concatenado

La primera vez hay que convertir el CSV de posts (690 MB) a parquet:

    python -m src.data
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from src.config import POSTS_CSV, POSTS_PARQUET, TEST_CSV, TRAIN_CSV, TRAITS, SEED


def preparar_posts(chunksize: int = 200_000) -> None:
    """Convierte posts_v2.csv en posts.parquet (username, body), por bloques."""
    POSTS_PARQUET.parent.mkdir(parents=True, exist_ok=True)
    schema = pa.schema([("username", pa.string()), ("body", pa.string())])
    n = 0
    with pq.ParquetWriter(POSTS_PARQUET, schema, compression="zstd") as writer:
        for chunk in pd.read_csv(POSTS_CSV, chunksize=chunksize, dtype=str, keep_default_na=False):
            writer.write_table(pa.Table.from_pandas(chunk[["username", "body"]], schema=schema, preserve_index=False))
            n += len(chunk)
    print(f"{n:,} posts guardados en {POSTS_PARQUET}")


def cargar_posts() -> pd.DataFrame:
    """Un post por fila: columnas username y body."""
    if not POSTS_PARQUET.exists():
        raise FileNotFoundError(f"No existe {POSTS_PARQUET}. Ejecuta antes: python -m src.data")
    return pd.read_parquet(POSTS_PARQUET)


def cargar_autores() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Devuelve (train, test) ordenados por username.

    En train algunos rasgos vienen vacíos (NaN): hay que ignorarlos al entrenar
    ese rasgo, no rellenarlos. En test todos los rasgos son NaN.
    """
    train = pd.read_csv(TRAIN_CSV).sort_values("username").reset_index(drop=True)
    test = pd.read_csv(TEST_CSV).sort_values("username").reset_index(drop=True)
    train[TRAITS] = train[TRAITS].astype(float)
    return train, test


def textos_por_usuario(max_posts: int | None = None, sep: str = "\n") -> pd.Series:
    """Texto de cada usuario (train + test) concatenando sus posts.

    max_posts: si se indica, toma como mucho ese número de posts por usuario
    (muestra aleatoria con SEED, reproducible). Los usuarios sin posts reciben "".
    """
    posts = cargar_posts()
    if max_posts is not None:
        rng = np.random.default_rng(SEED)
        posts = posts.assign(_r=rng.random(len(posts)))
        posts = posts.sort_values(["username", "_r"]).groupby("username").head(max_posts)
    textos = posts.groupby("username")["body"].agg(sep.join)

    train, test = cargar_autores()
    usuarios = pd.concat([train["username"], test["username"]])
    return textos.reindex(usuarios).fillna("")


if __name__ == "__main__":
    preparar_posts()
