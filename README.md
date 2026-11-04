# TecLin_Final_Boss

Predicción de los rasgos de personalidad Big Five a partir de posts de Reddit
(Práctica 4, Tecnologías del Lenguaje, USC 2026-27).

Las reglas de trabajo (para personas y agentes) están en [AGENTS.md](AGENTS.md).
Los resultados de cada variante, en [EXPERIMENTOS.md](EXPERIMENTOS.md).

## Puesta en marcha en local

1. Clonar el repo y crear el entorno:
   ```bash
   python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
   ```
2. Copiar (o enlazar) los tres CSV del enunciado en `data/raw/`:
   `posts_v2.csv`, `authors_train.csv`, `authors_test.csv`. La carpeta `data/` no se sube a git.
3. Convertir los posts a parquet (una sola vez, ~10 s, ~300 MB):
   ```bash
   .venv/bin/python -m src.data
   ```
4. Abrir `notebooks/00_plantilla.ipynb`, copiarlo como `notebooks/NN_autor_tema.ipynb` y trabajar ahí.

## Puesta en marcha en Colab

1. En Drive, una carpeta con `raw/` (los 3 CSV) y, tras el paso 3 de arriba, `processed/posts.parquet`.
   Se puede subir el parquet generado en local para no regenerarlo.
2. Abrir el notebook desde Colab (Archivo → Abrir cuaderno → GitHub). La primera celda clona el repo,
   monta Drive y apunta `TECLIN_DATA` a esa carpeta: solo hay que ajustar la ruta.
3. Para guardar: Archivo → Guardar una copia en GitHub, **en tu rama**, nunca en `main`.
   Si en Colab necesitas hacer push con git, usa un token guardado en los Secretos de Colab, nunca en el notebook.

## Flujo de trabajo

```bash
git switch main && git pull
git switch -c <nombre>/<tema>
# ... trabajar en tu notebook, apuntar el resultado en EXPERIMENTOS.md ...
git add -A && git commit -m "exp: <variante> (RMSE medio X.XX)"
git push -u origin <nombre>/<tema>
gh pr create
```

- PRs que tocan `src/`, `AGENTS.md` o las skills: las aprueba el compañero.
- PRs solo con tu notebook, `EXPERIMENTOS.md` o `submissions/`: puedes fusionarlas tú.
- Revisión cruzada: pide a tu agente "revisa la PR #N" (skill `revisar-pr`).

## Skills para los agentes

| Skill | Para qué | Cómo pedirlo |
|---|---|---|
| `experimento` | Implementar, evaluar y registrar una variante | Claude Code: `/experimento TF-IDF + Ridge` · Codex: "usa la skill experimento para…" |
| `revisar-pr` | Revisar la PR del compañero | `/revisar-pr 3` |
| `entrega` | Preparar y validar los CSV de un envío | `/entrega` |

Las instrucciones están en `.agents/skills/` (las lee Codex). `.claude/skills/` solo redirige a ellas,
así que cualquier cambio se hace en `.agents/skills/`.

## Fechas

| Fecha (23:59) | Qué |
|---|---|
| 19 nov | Primer envío de variantes (opcional) |
| 3 dic | Segundo envío (opcional) |
| **13 dic** | **Variantes finales (obligatorio)** |
| **14 dic** | **Notebook `<equipo>_reto.ipynb`** |
| 15-16 dic | Presentación |
