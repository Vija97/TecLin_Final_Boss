# Registro de experimentos

Una fila por variante evaluada con `src.evaluate.validacion_cruzada` (5 folds, SEED 42).
Se añade en el mismo commit que el notebook que la produce. Las que salen mal también se apuntan:
explican decisiones en el notebook final y la presentación.
"Variante" es el mismo nombre con el que se guardan sus predicciones en `predicciones/`.

| Fecha | Autor | Issue | Variante | Notebook | agre | open | cons | extr | neur | **Medio** | Notas (fugas declaradas, coste, conclusión) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-11-04 | Vija97 | — | media | `00_plantilla.ipynb` | 31.23 | 27.85 | 30.03 | 30.62 | 32.30 | **30.41** | Predice la media de train. Es lo mínimo que hay que batir. |
| 2026-11-18 | IagoVarelaR | #5 | sbert_minilm_p50_a10 | `notebooks/05_iago_sbert.ipynb` | 30.96 | 27.72 | 29.91 | 30.32 | 32.02 | **30.18** | MiniLM congelado; hasta 50 posts/usuario (69.472 posts), SEED 42, límite de 256 tokens; media por usuario y Ridge alpha=10. Los 39 usuarios sin posts reciben vector cero. Embeddings de train/test sin ajustar el encoder ni utilizar etiquetas. Generación y guardado: 74.9 s en RTX 3050 Laptop. Mejora de 0.224 frente a la media, no concluyente según el margen del equipo. |
| 2026-11-25 | Vija97 | #32 | tfidf_ridgecv | `notebooks/32_vija97_mbti.ipynb` | 29.75 | 26.96 | 29.39 | 28.73 | 31.19 | **29.20** | TF-IDF palabras (1-2) + caracteres (char_wb 2-5), hasta 500 posts/usuario, RidgeCV (alpha con validación interna, sin trampa). Vocabulario ajustado solo con el train de cada fold. ~12 min sin GPU. |
| 2026-11-25 | Vija97 | #32 | mbti_auto | `notebooks/32_vija97_mbti.ipynb` | 29.22 | 26.69 | 28.69 | 27.83 | 30.92 | **28.67** | `tfidf_ridgecv` + 4 letras del MBTI autoidentificado (+1/−1) e indicador. Tipo extraído del propio texto, sin etiquetas. −0,53, mejora en los 5 folds. |
| 2026-11-25 | Vija97 | #32 | mbti_auto_menc | `notebooks/32_vija97_mbti.ipynb` | 29.14 | 26.59 | 28.17 | 27.39 | 30.79 | **28.41** | Como `mbti_auto` y, si no hay autoidentificación, el tipo más mencionado (≥ 3 menciones, umbral fijado de antemano). Cobertura 32 % train / 26 % test. **−0,79**, mejora en los 5 folds. |

## Envíos

| Fecha de envío | Issue | Variantes enviadas | RMSE leaderboard | Comentario |
|---|---|---|---|---|
| 2026-11-19 | #6 | `tfidf_wordchar_ridge` (CV 29.18) · `sbert_minilm_p50_a10` (CV 30.18) · `tfidf_char_ridge` (CV 29.30) | word+char **29.140** · sbert **30.159** · char **29.184** (media del resto de equipos: 30.479) | **La CV coincide con la leaderboard** (diferencias ≤ 0,12): nos podemos fiar de la validación. Puesto 3 de 14 equipos (1º: 28.750). La leaderboard no cuenta los 10 usuarios de test sin posts. Objetivo: ver si la leaderboard se parece a la CV. Las TF-IDF salen de la PR #19 (commit `c995684`), con `alpha` elegido sobre los mismos folds: su CV puede ser algo optimista. |
