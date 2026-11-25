"""Limpieza de posts con reglas opcionales y combinables (#7).

Las reglas salen del análisis del texto (#21) y de las relaciones texto-rasgos (#22):

    from src.limpieza import limpiar_posts, REGLAS
    posts_limpios = limpiar_posts(cargar_posts(), reglas=("html", "vacios", "dedup"))
    textos = textos_por_usuario(max_posts=500, posts=posts_limpios)

Ninguna regla borra las menciones MBTI (#22). No hay regla para quitar citas de otros usuarios:
el dataset no tiene saltos de línea, así que no se sabe dónde termina una cita (`&gt;...`).
"""

from __future__ import annotations

import html
import re

import pandas as pd

REGLAS = ("html", "markdown", "urls", "vacios", "dedup")

_URL = re.compile(r"https?://\S+|www\.\S+")
_LINK_MD = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_MARCAS_MD = re.compile(r"\*\*|__|~~|`")


def limpiar_posts(posts: pd.DataFrame, reglas: tuple[str, ...] = REGLAS) -> pd.DataFrame:
    """Aplica las reglas indicadas, siempre en el mismo orden, y devuelve una copia.

    - html: decodifica entidades HTML (`&gt;` → `>`, `&amp;` → `&`).
    - markdown: `[texto](enlace)` → `texto` y quita `**`, `__`, `~~` y `` ` ``.
    - urls: sustituye cada URL por el token `URL`.
    - vacios: quita posts vacíos, `[deleted]` y `[removed]`.
    - dedup: deja una sola copia de cada post repetido exactamente por el mismo usuario.
    """
    desconocidas = set(reglas) - set(REGLAS)
    if desconocidas:
        raise ValueError(f"Reglas desconocidas: {sorted(desconocidas)}. Disponibles: {REGLAS}")
    out = posts[["username", "body"]].copy()
    body = out["body"].fillna("")
    if "html" in reglas:
        body = body.map(html.unescape)
    if "markdown" in reglas:
        body = body.str.replace(_LINK_MD, r"\1", regex=True).str.replace(_MARCAS_MD, "", regex=True)
    if "urls" in reglas:
        body = body.str.replace(_URL, " URL ", regex=True)
    out["body"] = body
    if "vacios" in reglas:
        s = out["body"].str.strip()
        out = out[(s != "") & ~s.isin(["[deleted]", "[removed]"])]
    if "dedup" in reglas:
        out = out.drop_duplicates(["username", "body"])
    return out.reset_index(drop=True)
