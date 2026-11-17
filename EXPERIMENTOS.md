# Registro de experimentos

Una fila por variante evaluada con `src.evaluate.validacion_cruzada` (5 folds, SEED 42).
Se añade en el mismo commit que el notebook que la produce. Las que salen mal también se apuntan:
explican decisiones en el notebook final y la presentación.
"Variante" es el mismo nombre con el que se guardan sus predicciones en `predicciones/`.

| Fecha | Autor | Issue | Variante | Notebook | agre | open | cons | extr | neur | **Medio** | Notas (fugas declaradas, coste, conclusión) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-11-04 | Vija97 | — | media | `00_plantilla.ipynb` | 31.23 | 27.85 | 30.03 | 30.62 | 32.30 | **30.41** | Predice la media de train. Es lo mínimo que hay que batir. |
| 2026-11-17 | Jesusrf21 | #4 | tfidf_word_ridge | `04_jesus_tfidf.ipynb` | 29.92 | 27.03 | 29.41 | 28.80 | 31.38 | **29.31** | TF-IDF palabras (1-2 gramas, min_df=3, 100k términos, sublinear_tf) + Ridge por rasgo, max_posts=500. alpha elegido 0.1 con los mismos folds (optimista): 0.03 → 29.311, 0.1 → 29.309, 0.3 → 29.331, 1 → 29.474. Con max_posts=200: 29.40 (alpha 0.1). Sin fuga (vectorizador ajustado solo con train de cada fold). ~1 min de TF-IDF, sin GPU. |
| 2026-11-17 | Jesusrf21 | #4 | tfidf_char_ridge | `04_jesus_tfidf.ipynb` | 29.88 | 27.02 | 29.46 | 28.98 | 31.16 | **29.30** | TF-IDF n-gramas de caracteres (char_wb 2-5, min_df=3, 200k términos, sublinear_tf) + Ridge, max_posts=500. alpha elegido 0.3 con los mismos folds (optimista): 0.1 → 29.351, 0.3 → 29.299, 1 → 29.409. Con max_posts=200: 29.43 (alpha 0.3). Sin fuga. ~4 min de TF-IDF en paralelo. Igual que palabras (diferencia dentro del ruido). |
| 2026-11-17 | Jesusrf21 | #4 | tfidf_wordchar_ridge | `04_jesus_tfidf.ipynb` | 29.73 | 26.94 | 29.37 | 28.72 | 31.14 | **29.18** | Palabras + caracteres (hstack de las dos anteriores) + Ridge, max_posts=500. alpha elegido 0.1 con los mismos folds (optimista): 0.1 → 29.181, 0.3 → 29.187, 1 → 29.265. Con max_posts=200: 29.29. Mejora a la media en los 5 folds (1,1-1,5 por fold); frente a word/char solo ~0,1 (ruido). Sin fuga. |

## Envíos

| Fecha de envío | Issue | Variantes enviadas | RMSE leaderboard | Comentario |
|---|---|---|---|---|
