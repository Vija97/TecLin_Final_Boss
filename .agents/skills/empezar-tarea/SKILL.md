---
name: empezar-tarea
description: "Empezar una tarea a partir de su GitHub Issue: comprobar dependencias, crear la rama desde main actualizado, preparar el notebook desde la plantilla y resumir qué hay que hacer. Usar cuando alguien diga que empieza una Issue (p. ej. 'empiezo la #4')."
---

# Empezar una tarea

Entrada: número de Issue (`#4` o `4`). Objetivo: dejar a la persona trabajando en un par de minutos,
en la rama correcta y sabiendo qué hay que hacer. **No implementar nada aquí.**
Leer antes [AGENTS.md](../../../AGENTS.md).

## Pasos

1. **Estado limpio.** `git status --short --branch`. Si hay cambios sin commitear o una operación de git
   a medias (merge, rebase), parar y explicarlo.
2. **Leer la Issue.** `gh issue view <n>`: título, responsable, hito, etiquetas, checklist y "Depende de".
   - Si no existe o está cerrada, parar.
   - Si la persona no es la responsable, avisar antes de seguir (puede ser intencionado).
   - Si tiene la etiqueta `gpu` y la persona no tiene GPU (ver tabla "Equipo" de `AGENTS.md`), avisar.
   - Para cada Issue de "Depende de": si sigue abierta, decir qué falta y si se puede avanzar igualmente.
   - No crear Issues sin que la persona lo pida.
3. **Rama desde `main` actualizado:**
   ```bash
   git switch main && git pull --ff-only
   git switch -c <usuario>/<n>-<tema-corto>        # p. ej. jesus/4-tfidf
   ```
   Si la rama ya existe, cambiar a ella (`git switch <rama>`) en vez de crearla. Si `pull --ff-only` falla, parar.
   Si `main` todavía no tiene `src/` (la base común no se ha fusionado), avisar y partir de la rama que la
   contenga, diciéndolo explícitamente.
4. **Notebook** (solo si la Issue tiene la etiqueta `variante` o `datos`): si no existe ya
   `notebooks/<NN>_<autor>_<tema>.ipynb` (NN = número de Issue con dos cifras), copiar
   `notebooks/00_plantilla.ipynb` con ese nombre y rellenar la cabecera (autor, Issue, variante).
   No ejecutar nada todavía.
5. **Contexto.** Leer `EXPERIMENTOS.md` (mejor RMSE hasta ahora y variantes con predicciones en `predicciones/`)
   y las partes de `AGENTS.md` que aplican (evaluación y fugas si es una variante, entregas si es un envío).
   Si la tarea necesita algo caro (embeddings, fine-tuning, LLM), recordar que hay que estimar tiempo/coste
   antes y si hay cachés en el Drive compartido (`data/processed/`).
6. **Informar:** Issue y responsable, rama, notebook creado, dependencias pendientes, la checklist de la Issue
   como plan, cómo se sabrá que está hecha ("Hecho cuando") y la skill que toca después
   (`experimento` para variantes, `entrega` para envíos).
