---
name: revisar-pr
description: "Revisar una Pull Request del compañero: fugas de datos, uso de la evaluación común, reproducibilidad y formato. Usar cuando se pida revisar una PR o la rama de la otra persona."
---

# Revisar una PR

Entrada: número de PR (o rama). Leer antes [AGENTS.md](../../../AGENTS.md).

## Pasos

1. Leer la PR y su diff: `gh pr view <n>` y `gh pr diff <n>`. Si hay notebooks, leer sus celdas de código
   y las salidas guardadas, no solo el JSON del diff.
2. Revisar, por orden de gravedad:

   **Bloqueantes**
   - **Fuga de etiquetas**: algo que use las etiquetas de validación o test dentro de `fit_predict`
     (modelo, selección de features, normalización del objetivo, búsqueda de hiperparámetros sobre
     los mismos folds de la evaluación sin anidar, early stopping con el fold de validación…).
   - La cifra no sale de `src.evaluate.validacion_cruzada`, o se han cambiado folds, semilla o métrica.
   - La fila de `EXPERIMENTOS.md` no coincide con la salida guardada en el notebook.
   - Cambios en `src/` que rompen la firma o el comportamiento que usan los notebooks del otro.
   - Datos, parquet, embeddings, claves o tokens añadidos al repo.

   **Importantes**
   - Ajustes sin etiquetas sobre textos de validación/test no declarados en `EXPERIMENTOS.md`.
   - Semillas sin fijar; resultados que no se pueden reproducir.
   - El notebook no corre de arriba abajo, no tiene salidas guardadas o edita un notebook ajeno.
   - Una mejora < ~0,3 de RMSE medio presentada como clara.
   - Usuarios sin posts o etiquetas NaN mal tratados.

   **Menores**
   - Falta explicación en celdas de texto; código que debería ir a `src/`; nombres de ficheros.
3. Si se puede, ejecutar lo que cambia (p. ej. `python -m src.submission <csv>` o la celda de evaluación
   con `max_posts` reducido) y decir qué se ha ejecutado y qué no.

## Resultado

Redactar la revisión con: veredicto (aprobable / cambios necesarios), lista de hallazgos con
fichero/celda y por qué importan, y qué se verificó ejecutando. **Mostrarla a la persona primero.**
Solo publicarla en GitHub (`gh pr review <n> --comment --body ...`) si la persona lo pide.
Nunca aprobar ni fusionar: eso lo hace la persona.
