import pandas as pd

from src import artefacto
from src.variables import CARACTERISTICAS, RUTA_DATOS, UMBRAL_HIT


def test_artefacto_tiene_ambos_modelos():
    art = artefacto.cargar()
    assert artefacto.obtener_pipeline(art, artefacto.REGRESION) is not None
    assert artefacto.obtener_pipeline(art, artefacto.CLASIFICACION) is not None
    assert art["metadatos"]["caracteristicas"] == CARACTERISTICAS


def test_sin_fuga_de_datos():
    assert "es_hit" not in CARACTERISTICAS
    assert "reproducciones_sem1" not in CARACTERISTICAS
    assert "popularidad" not in CARACTERISTICAS


def test_es_hit_coincide_con_umbral():
    df = pd.read_csv(RUTA_DATOS)
    assert ((df["popularidad"] >= UMBRAL_HIT).astype(int) == df["es_hit"]).all()


def test_metricas_minimas():
    art = artefacto.cargar()
    assert art[artefacto.REGRESION]["metricas"]["R2_test"] > 0.5
    assert art[artefacto.CLASIFICACION]["metricas"]["AUC_test"] > 0.8
