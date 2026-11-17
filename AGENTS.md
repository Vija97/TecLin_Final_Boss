# Reglas del proyecto (personas y agentes)

Este fichero lo leen Claude Code (vía `CLAUDE.md`) y Codex. Si cambia una regla,
se cambia aquí y en ningún otro sitio.

## El problema en 5 líneas

- Práctica 4 de Tecnologías del Lenguaje (USC 2026-27): predecir los 5 rasgos Big Five
  (`agreeableness, openness, conscientiousness, extraversion, neuroticism`, de 0 a 100)
  de usuarios de Reddit a partir de sus posts.
- Métrica: **RMSE medio de los 5 rasgos** (menos es mejor). Predecir la media da ≈ 30,4.
- Datos: 1.288 usuarios de train (algunos rasgos vacíos), 323 de test, 3,1 M posts.
  39 usuarios no tienen ningún post.
- Se evalúa el **notebook final explicado** y la **presentación**, no la posición en la leaderboard.

## Equipo

| GitHub | Agente | Máquina |
|---|---|---|
| `Vija97` | Claude Code | GPU |
| `IagoVarelaR` | Codex | GPU |
| `Jesusrf21` | Claude Code | **Sin GPU**: no asignarle tareas que necesiten GPU |

Vamos **con margen**: plazos internos varios días antes de los oficiales (ver "Entregas").

## Estructura

```text
src/config.py       rutas, TRAITS, TEAM_NAME, SEED, N_FOLDS
src/data.py         cargar_autores(), cargar_posts(), textos_por_usuario()
src/evaluate.py     validacion_cruzada(), PorRasgo, rmse_por_rasgo()
src/predicciones.py guardar_predicciones(), cargar_predicciones() (para combinar variantes)
src/submission.py   generar_entrega(), entrega_desde_predicciones(), validar_entrega()
notebooks/          un notebook por variante o idea, cada uno con un único dueño
predicciones/       OOF y test de cada variante (CSV pequeños, se suben)
submissions/        CSV enviados (formato del enunciado)
EXPERIMENTOS.md     registro de TODAS las variantes evaluadas
data/               no se sube a git (ver README)
```

## Regla de oro: cómo se evalúa

1. Toda variante se mide con `src.evaluate.validacion_cruzada` sin modificarla:
   mismos 5 folds, misma semilla. Un RMSE calculado de otra forma no se compara ni se apunta.
2. La variante es una función `fit_predict(train_df, val_df) -> array (n_val, 5)` en el orden de `TRAITS`.
3. **Fuga de datos = resultado inválido.** Dentro de `fit_predict`, todo lo que use etiquetas
   (modelo, selección de features por correlación, calibración, early stopping…) se ajusta
   solo con `train_df`. Ajustar algo sin etiquetas con textos de validación/test
   (p. ej. el vocabulario de TF-IDF) se permite solo si se declara en `EXPERIMENTOS.md`.
4. Las etiquetas vacías (NaN) se ignoran por rasgo (`PorRasgo` ya lo hace); no se rellenan.
5. Cada variante terminada guarda sus predicciones con `guardar_predicciones` (OOF de la validación
   cruzada + test entrenando con todo train). Así se pueden combinar y enviar sin reentrenar.
6. Cada resultado se apunta en `EXPERIMENTOS.md` en el mismo commit que el notebook que lo produce.
   Diferencias menores de ~0,3 de RMSE medio son ruido entre folds: no se venden como mejora.

## Issues, ramas y PRs

- **Cada tarea es una GitHub Issue** con responsable y hito (Envío 1, Envío 2, Final).
  Antes de empezar algo, comprobar que hay una Issue; si no la hay, se crea (con permiso de la persona).
- Ramas: `<nombre>/<issue>-<tema>` (p. ej. `jesus/4-tfidf`). Nada se sube directo a `main`
  (está protegida).
- Todo entra por Pull Request, y la PR lleva `Closes #N` de su Issue.
  - Cambios en `src/`, `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/` o `.github/`:
    **los aprueba otra persona del equipo** (lo exige `CODEOWNERS`). Un fallo ahí invalida las comparaciones de todos.
  - Notebooks propios, `EXPERIMENTOS.md`, `predicciones/` y `submissions/`: el autor puede fusionar su PR.
- Revisión cruzada: el agente de una persona revisa las PRs de otra con la skill `revisar-pr`.
- Commits: `tipo(#issue): descripción` en español (`feat`, `fix`, `exp`, `docs`, `chore`).
  `exp:` = experimento nuevo con su fila en `EXPERIMENTOS.md`.

## Notebooks

- Nombre: `notebooks/NN_autor_tema.ipynb` (p. ej. `04_jesus_tfidf.ipynb`, con NN = número de la Issue).
  Se parte de `00_plantilla.ipynb`.
- **Un único dueño por notebook**: nadie (ni su agente) edita el notebook de otro.
- Se suben **ejecutados y con las salidas guardadas** (la entrega final lo exige), de arriba abajo sin errores.
  Sin imprimir textos largos ni dataframes enormes: el `.ipynb` debe pesar poco.
- Celdas de texto explicando qué se prueba y por qué: así el notebook final se monta copiando.
- La lógica reutilizable sube a `src/` (con PR y aprobación); el notebook la importa.
- Memoria: el texto completo de todos los usuarios ocupa ~5,5 GB de RAM (un usuario tiene 15,8 M de caracteres).
  En portátiles con poca RAM usar `textos_por_usuario(max_posts=...)`.

## Reglas específicas para agentes

- No inventar ni redondear resultados: solo se apuntan cifras que salen de `validacion_cruzada` en una ejecución real.
- No tocar `src/evaluate.py` ni los folds para "mejorar" una cifra.
- No subir datos (`data/`, parquet, embeddings), claves de API ni tokens. Las claves van en variables de entorno o en los Secretos de Colab.
- No fusionar ni aprobar PRs; no publicar comentarios ni crear o cerrar Issues en GitHub sin que la persona lo pida.
- Antes de lanzar algo largo (embeddings de 3 M posts, fine-tuning, llamadas a un LLM de pago),
  estimar tiempo/coste y preguntar. Cachear resultados caros en `data/processed/` (o en el Drive compartido).
- Si una petición choca con estas reglas, avisarlo en vez de saltárselas.

## Entregas

| Qué | Oficial (23:59) | **Interno** |
|---|---|---|
| Envío 1 (opcional) | 19 nov | 19 nov |
| Envío 2 (opcional) | 3 dic | 1 dic |
| Envío final (obligatorio) | 13 dic | **8 dic** |
| Notebook `FinalBoss_reto.ipynb` | 14 dic | **10 dic** |
| Presentación | 15-16 dic | **12 dic** (ensayada) |

- 2 o 3 variantes por envío. Fichero `<TEAM_NAME>_<variante>.csv` con las columnas
  `team_name,variant_name,username,agreeableness,openness,conscientiousness,extraversion,neuroticism`.
- Se generan con `src.submission` (ya valida). Ver la skill `entrega`.

## Skills

Están en `.agents/skills/` (Codex las lee ahí; `.claude/skills/` solo redirige a ellas):

- `experimento`: implementar y evaluar una variante, guardar sus predicciones y registrarla.
- `revisar-pr`: revisar la PR de otra persona (fugas, evaluación, reproducibilidad).
- `entrega`: preparar y validar los CSV de un envío.
