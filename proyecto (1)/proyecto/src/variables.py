"""Constantes compartidas: rutas, nombres de columnas y categorías."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RUTA_DATOS = RAIZ / "data" / "canciones.csv"
RUTA_MODELO = RAIZ / "models" / "modelo.pkl"

SEMILLA = 42

# Solo características conocidas ANTES del lanzamiento.
# Se excluyen a propósito (fuga de datos):
#   - reproducciones_sem1: solo existe después de publicar la canción.
#   - es_hit: se deriva de la popularidad (popularidad >= UMBRAL_HIT).
NUMERICAS = [
    "bailabilidad", "energia", "valencia", "acustica", "tempo",
    "duracion_min", "volumen_db", "anio", "colaboracion",
]
CATEGORICAS = ["genero"]
CARACTERISTICAS = NUMERICAS + CATEGORICAS

GENEROS = ["pop", "urbano", "rock", "electronica", "indie"]

OBJETIVO_REGRESION = "popularidad"
OBJETIVO_CLASIFICACION = "es_hit"
UMBRAL_HIT = 70
