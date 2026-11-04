---
name: experimento
description: "Implementar, evaluar con la validación cruzada común y registrar en EXPERIMENTOS.md una variante para predecir Big Five. Usar cuando se pida probar una idea, modelo o mejora."
---

# Experimento

Entrada: la idea a probar (p. ej. "TF-IDF + Ridge", "SBERT medio por usuario") y, si existe,
el notebook donde va. Leer antes [AGENTS.md](../../../AGENTS.md).

## Pasos

1. **Dónde.** Confirmar quién es el autor y usar su propio notebook (`notebooks/NN_autor_tema.ipynb`),
   creado a partir de `notebooks/00_plantilla.ipynb` si es nuevo. Nunca editar el notebook de la otra persona.
   Trabajar en una rama `<autor>/<tema>`, no en `main`.
2. **Coste.** Si la variante tarda más de unos minutos o cuesta dinero (embeddings de todos los posts,
   fine-tuning, LLM por API), estimar tiempo/coste, proponer una versión reducida
   (`textos_por_usuario(max_posts=...)`, subconjunto de usuarios) y preguntar antes de lanzarla.
   Cachear lo caro en `data/processed/` (nunca en git).
3. **Implementar** `fit_predict(train_df, val_df) -> np.ndarray (len(val_df), 5)` en el orden de `TRAITS`:
   - todo lo que use etiquetas se ajusta solo con `train_df`;
   - NaN en las etiquetas: usar `PorRasgo` o filtrar por rasgo, nunca rellenar;
   - semillas fijadas con `SEED`.
   Si algo sin etiquetas se ajusta con textos de validación/test, anotarlo para declararlo.
4. **Evaluar** con `validacion_cruzada(fit_predict, train, nombre="...")`. No cambiar folds ni semilla.
5. **Comparar** con la mejor fila de `EXPERIMENTOS.md`. Mirar también la dispersión entre folds:
   diferencias < ~0,3 en el RMSE medio son ruido. Decirlo así, sin exagerar.
6. **Registrar** una fila en `EXPERIMENTOS.md` con las cifras que imprime `validacion_cruzada`
   (copiadas, no redondeadas a mano), la ruta del notebook y notas (fugas declaradas, tiempo, conclusión).
   Añadir en el notebook una celda de texto con qué se probó, por qué y qué salió.
7. **Notebook limpio.** Ejecutarlo de arriba abajo sin errores, guardado con salidas y sin volcados enormes.
8. **Commit** `exp: <variante> (RMSE medio X.XX)` con notebook + `EXPERIMENTOS.md`, push y PR si se pide.
   Si se tocó `src/`, la PR necesita la aprobación del compañero.

## Al terminar, informar

- RMSE medio y por rasgo, y la diferencia con la mejor variante hasta ahora.
- Qué no se ha comprobado o qué queda pendiente.
- Si hay algo que revisar por posible fuga de datos.
