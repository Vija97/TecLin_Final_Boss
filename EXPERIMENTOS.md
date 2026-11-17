# Registro de experimentos

Una fila por variante evaluada con `src.evaluate.validacion_cruzada` (5 folds, SEED 42).
Se añade en el mismo commit que el notebook que la produce. Las que salen mal también se apuntan:
explican decisiones en el notebook final y la presentación.
"Variante" es el mismo nombre con el que se guardan sus predicciones en `predicciones/`.

| Fecha | Autor | Issue | Variante | Notebook | agre | open | cons | extr | neur | **Medio** | Notas (fugas declaradas, coste, conclusión) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-11-04 | Vija97 | — | media | `00_plantilla.ipynb` | 31.23 | 27.85 | 30.03 | 30.62 | 32.30 | **30.41** | Predice la media de train. Es lo mínimo que hay que batir. |

## Envíos

| Fecha de envío | Issue | Variantes enviadas | RMSE leaderboard | Comentario |
|---|---|---|---|---|
