"""API de predicción de popularidad de canciones.

Local:   uvicorn src.app.main:app --reload     (docs en /docs)
Render:  uvicorn src.app.main:app --host 0.0.0.0 --port $PORT
"""
from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse

from src import artefacto
from src.app.schemas import Cancion, Prediccion
from src.variables import CARACTERISTICAS

app = FastAPI(
    title="Servicio de predicción de popularidad de canciones",
    description="Recibe características de una canción y devuelve su popularidad "
                "estimada (regresión) y la probabilidad de que sea un hit (clasificación).",
    version="1.0.0",
)

_artefacto = artefacto.cargar()
_regresor = artefacto.obtener_pipeline(_artefacto, artefacto.REGRESION)
_clasificador = artefacto.obtener_pipeline(_artefacto, artefacto.CLASIFICACION)


PAGINA = Path(__file__).parent / "static" / "index.html"


@app.get("/", include_in_schema=False)
def pagina_principal():
    """Interfaz web (Hit Lab) para probar el modelo desde el navegador."""
    return FileResponse(PAGINA)


@app.get("/api")
def api_info():
    return {"mensaje": "API activa. Usa POST /predict o visita /docs"}


@app.get("/salud")
def salud():
    return {
        "estado": "ok" if _regresor is not None else "sin modelo",
        "regresion": _regresor is not None,
        "clasificacion": _clasificador is not None,
    }


@app.get("/modelo")
def info_modelo():
    """Metadatos y métricas del modelo cargado."""
    return {
        "metadatos": _artefacto.get("metadatos", {}),
        "regresion": _artefacto.get(artefacto.REGRESION, {}).get("metricas"),
        "clasificacion": _artefacto.get(artefacto.CLASIFICACION, {}).get("metricas"),
    }


@app.post("/predict", response_model=Prediccion)
def predecir(cancion: Cancion):
    datos = pd.DataFrame([cancion.model_dump(mode="json")])[CARACTERISTICAS]
    popularidad = float(_regresor.predict(datos)[0])
    respuesta = {"popularidad_estimada": round(max(0.0, min(100.0, popularidad)), 1)}
    if _clasificador is not None:
        proba = float(_clasificador.predict_proba(datos)[0, 1])
        respuesta["probabilidad_hit"] = round(proba, 3)
        respuesta["es_hit_predicho"] = proba >= 0.5
    return respuesta
