import pytest
from fastapi.testclient import TestClient

from src.app.main import app

CANCION = {
    "bailabilidad": 0.78, "energia": 0.87, "valencia": 0.4, "acustica": 0.45,
    "tempo": 137, "duracion_min": 3.5, "volumen_db": -5.3, "anio": 2020,
    "colaboracion": 1, "genero": "pop",
}


@pytest.fixture(scope="module")
def cliente():
    return TestClient(app)


def test_pagina_principal(cliente):
    r = cliente.get("/")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
    assert "Hit Lab" in r.text


def test_api_info(cliente):
    assert cliente.get("/api").status_code == 200


def test_salud(cliente):
    r = cliente.get("/salud")
    assert r.status_code == 200
    assert r.json()["estado"] == "ok"


def test_prediccion_valida(cliente):
    r = cliente.post("/predict", json=CANCION)
    assert r.status_code == 200
    cuerpo = r.json()
    assert 0 <= cuerpo["popularidad_estimada"] <= 100
    assert 0 <= cuerpo["probabilidad_hit"] <= 1
    assert isinstance(cuerpo["es_hit_predicho"], bool)


def test_mas_baile_y_energia_sube_popularidad(cliente):
    alta = cliente.post("/predict", json=CANCION).json()
    baja = cliente.post(
        "/predict", json={**CANCION, "bailabilidad": 0.2, "energia": 0.1}
    ).json()
    assert alta["popularidad_estimada"] > baja["popularidad_estimada"]


@pytest.mark.parametrize("cambio", [
    {"genero": "jazz"},        # género desconocido
    {"energia": 1.5},          # fuera de rango
    {"colaboracion": 2},       # solo 0 o 1
])
def test_entradas_invalidas(cliente, cambio):
    r = cliente.post("/predict", json={**CANCION, **cambio})
    assert r.status_code == 422


def test_campo_faltante(cliente):
    datos = {k: v for k, v in CANCION.items() if k != "tempo"}
    assert cliente.post("/predict", json=datos).status_code == 422
