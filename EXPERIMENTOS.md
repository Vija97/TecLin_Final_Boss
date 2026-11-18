# Registro de experimentos

Una fila por variante evaluada con `src.evaluate.validacion_cruzada` (5 folds, SEED 42).
Se añade en el mismo commit que el notebook que la produce. Las que salen mal también se apuntan:
explican decisiones en el notebook final y la presentación.
"Variante" es el mismo nombre con el que se guardan sus predicciones en `predicciones/`.

| Fecha | Autor | Issue | Variante | Notebook | agre | open | cons | extr | neur | **Medio** | Notas (fugas declaradas, coste, conclusión) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-11-04 | Vija97 | — | media | `00_plantilla.ipynb` | 31.23 | 27.85 | 30.03 | 30.62 | 32.30 | **30.41** | Predice la media de train. Es lo mínimo que hay que batir. |
| 2026-11-18 | IagoVarelaR | #5 | sbert_minilm_p50_a10 | `notebooks/05_iago_sbert.ipynb` | 30.96 | 27.72 | 29.91 | 30.32 | 32.02 | **30.18** | MiniLM congelado; hasta 50 posts/usuario (69.472 posts), SEED 42, límite de 256 tokens; media por usuario y Ridge alpha=10. Los 39 usuarios sin posts reciben vector cero. Embeddings de train/test sin ajustar el encoder ni utilizar etiquetas. Generación y guardado: 74.9 s en RTX 3050 Laptop. Mejora de 0.224 frente a la media, no concluyente según el margen del equipo. |

## Envíos

| Fecha de envío | Issue | Variantes enviadas | RMSE leaderboard | Comentario |
|---|---|---|---|---|
