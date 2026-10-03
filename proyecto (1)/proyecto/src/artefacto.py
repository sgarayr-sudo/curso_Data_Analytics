"""Guardado y carga del artefacto del modelo (models/modelo.pkl).

El .pkl es un diccionario con los pipelines ya entrenados (preprocesamiento
incluido) y metadatos. Así regresión y clasificación comparten un solo archivo
y cada script de entrenamiento solo actualiza su parte.
"""
from datetime import datetime, timezone

import joblib
import sklearn

from src.variables import CARACTERISTICAS, RUTA_MODELO, UMBRAL_HIT

REGRESION = "regresion"
CLASIFICACION = "clasificacion"


def cargar(ruta=RUTA_MODELO) -> dict:
    """Carga el artefacto; si no existe devuelve uno vacío."""
    if ruta.exists():
        return joblib.load(ruta)
    return {"metadatos": {}}


def guardar_parte(nombre: str, pipeline, metricas: dict, ruta=RUTA_MODELO) -> None:
    """Actualiza una parte del artefacto (regresion o clasificacion) y lo guarda."""
    artefacto = cargar(ruta)
    artefacto[nombre] = {"pipeline": pipeline, "metricas": metricas}
    artefacto["metadatos"] = {
        "caracteristicas": CARACTERISTICAS,
        "umbral_hit": UMBRAL_HIT,
        "version_sklearn": sklearn.__version__,
        "actualizado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    ruta.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artefacto, ruta)


def obtener_pipeline(artefacto: dict, nombre: str):
    """Devuelve el pipeline de una parte, o None si no fue entrenada."""
    parte = artefacto.get(nombre)
    return parte["pipeline"] if parte else None
