---
name: entrega
description: "Preparar y validar los CSV de un envío de variantes a la competición (2-3 por fecha). Usar cuando se pida generar, revisar o preparar una entrega."
---

# Preparar un envío

Leer antes [AGENTS.md](../../../AGENTS.md) (sección Entregas).

## Pasos

1. **Elegir variantes** (2 o 3) con la persona, a partir de `EXPERIMENTOS.md`. Proponer las de mejor RMSE
   de validación, intentando que sean distintas entre sí (así la leaderboard enseña algo).
2. **Generar el CSV** de cada variante. Si tiene predicciones guardadas (`listar_variantes()`):
   `entrega_desde_predicciones("<variante>")`. Si no, entrenar con todo train
   (`preds = fit_predict(train, test)`) y `generar_entrega(test, preds, "<variante>")`.
   El nombre de la variante: solo letras, números, `-` y `_`.
3. **Validar** todos los ficheros: `python -m src.submission submissions/<TEAM_NAME>_*.csv`.
   Comprueba columnas, los 323 usuarios, sin NaN ni duplicados y valores en [0, 100].
   Revisar también que `TEAM_NAME` en `src/config.py` es el nombre registrado del equipo.
4. **Registrar** en la tabla "Envíos" de `EXPERIMENTOS.md` la fecha y las variantes enviadas.
5. **Commit** `chore(#issue): envío <fecha>` con los CSV y `EXPERIMENTOS.md`, en la rama de la Issue del envío.
6. Recordar a la persona que el envío lo hace ella por el canal que indique el profesor, y que
   cuando salga la leaderboard apunte el RMSE de cada variante en la tabla de Envíos.

Fechas oficiales (23:59): 19 nov, 3 dic, **13 dic (obligatoria)**; notebook final 14 dic.
Plazos internos del equipo (vamos con margen): envío final **8 dic**, notebook **10 dic** (ver `AGENTS.md`).
