"""Rutas y constantes compartidas por todo el proyecto."""

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# En local los datos van en <repo>/data. En Colab, apunta TECLIN_DATA a la
# carpeta de Drive que tenga raw/ y processed/.
DATA_DIR = Path(os.environ.get("TECLIN_DATA", REPO_ROOT / "data"))
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
SUBMISSIONS_DIR = REPO_ROOT / "submissions"

POSTS_CSV = RAW_DIR / "posts_v2.csv"
TRAIN_CSV = RAW_DIR / "authors_train.csv"
TEST_CSV = RAW_DIR / "authors_test.csv"
POSTS_PARQUET = PROCESSED_DIR / "posts.parquet"

# Mismo orden que en los CSV del enunciado y en el fichero de entrega.
TRAITS = ["agreeableness", "openness", "conscientiousness", "extraversion", "neuroticism"]

# Nombre del equipo tal y como se registró en el formulario.
TEAM_NAME = "FinalBoss"

# Fijos para que todas las variantes se comparen con los mismos folds.
SEED = 42
N_FOLDS = 5
