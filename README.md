# TecLin_Final_Boss

Predicción de los rasgos de personalidad Big Five a partir de posts de Reddit
(Práctica 4, Tecnologías del Lenguaje, USC 2026-27). Equipo **FinalBoss**: `Vija97`, `IagoVarelaR`, `Jesusrf21`.

- Reglas de trabajo (para personas y agentes): [AGENTS.md](AGENTS.md).
- Resultados de cada variante: [EXPERIMENTOS.md](EXPERIMENTOS.md).
- Tareas: [Issues](https://github.com/Vija97/TecLin_Final_Boss/issues), agrupadas por hito
  (Envío 1, Envío 2, Final). Cada una tiene responsable.

## Datos

Los datos no se suben a git (`posts_v2.csv` pesa 690 MB). Están en la **carpeta compartida de Drive**,
con esta estructura (es la que espera el código):

```text
data/
├── raw/         posts_v2.csv, authors_train.csv, authors_test.csv
└── processed/   posts.parquet (generado con `python -m src.data`) y cachés (embeddings…)
```

## Puesta en marcha en local

1. Clonar el repo y crear el entorno:
   ```bash
   python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
   ```
2. Copiar la carpeta `data/` del Drive dentro del repo (o solo `raw/` y luego el paso 3).
3. Si no tienes `processed/posts.parquet`, generarlo (una vez, ~10 s):
   ```bash
   .venv/bin/python -m src.data
   ```
4. Ejecutar `notebooks/00_plantilla.ipynb`: debe dar RMSE medio **30.41**.

**Memoria:** el texto completo de todos los usuarios ocupa ~5,5 GB de RAM. Con poca RAM usa
`textos_por_usuario(max_posts=...)`.

## Puesta en marcha en Colab

En Colab el repo se clona **dentro de tu Drive**: así los notebooks, `EXPERIMENTOS.md`, las predicciones
y los CSV no se pierden al cerrar la sesión.

1. Añade a tu Drive un acceso directo a la carpeta compartida `data/`.
2. Crea un token de GitHub (Settings → Developer settings → Fine-grained tokens, solo este repo,
   *Contents: Read and write*) y guárdalo en los **Secretos de Colab** (🔑) como `GH_TOKEN`.
   Nunca lo pegues en una celda.
3. Abre `00_plantilla.ipynb` en Colab y ejecuta la primera celda, ajustando `DRIVE_DATA` y `DRIVE_REPO`.
   La primera vez clona el repo en tu Drive.
4. A partir de ahí, abre tus notebooks **desde la copia del Drive** (no desde GitHub).
   La última celda de la plantilla hace commit y push a tu rama.

## Flujo de trabajo

```bash
git switch main && git pull
git switch -c <nombre>/<issue>-<tema>          # p. ej. jesus/4-tfidf
# ... trabajar en tu notebook; apuntar el resultado en EXPERIMENTOS.md; guardar predicciones ...
git add -A && git commit -m "exp(#4): tfidf_ridge (RMSE medio X.XX)"
git push -u origin <nombre>/<issue>-<tema>
gh pr create                                   # la plantilla pide "Closes #<issue>"
```

- `main` está protegida: todo entra por PR.
- PRs que tocan `src/`, `AGENTS.md`, las skills o `.github/`: necesitan la aprobación de otra persona (`CODEOWNERS`).
- PRs solo con tu notebook, `EXPERIMENTOS.md`, `predicciones/` o `submissions/`: puedes fusionarlas tú.
- Revisión cruzada: pide a tu agente "revisa la PR #N" (skill `revisar-pr`).

## Skills para los agentes

| Skill | Para qué | Cómo pedirlo |
|---|---|---|
| `experimento` | Implementar, evaluar, guardar predicciones y registrar una variante | Claude Code: `/experimento TF-IDF + Ridge` · Codex: "usa la skill experimento para…" |
| `revisar-pr` | Revisar la PR de otra persona | `/revisar-pr 3` |
| `entrega` | Preparar y validar los CSV de un envío | `/entrega` |

Las instrucciones están en `.agents/skills/` (las lee Codex). `.claude/skills/` solo redirige a ellas,
así que cualquier cambio se hace en `.agents/skills/`.

## Fechas

| Qué | Oficial (23:59) | Interno |
|---|---|---|
| Envío 1 (opcional) | 19 nov | 19 nov |
| Envío 2 (opcional) | 3 dic | 1 dic |
| **Envío final (obligatorio)** | **13 dic** | **8 dic** |
| **Notebook `FinalBoss_reto.ipynb`** | **14 dic** | **10 dic** |
| Presentación | 15-16 dic | 12 dic (ensayada) |
