"""Prueba un servicio desplegado (localhost o Render) con canciones de ejemplo.

Uso:
    python -m src.probar_servicio                          # http://127.0.0.1:8000
    python -m src.probar_servicio https://tu-app.onrender.com
"""
import json
import sys
import urllib.error
import urllib.request

EJEMPLOS = {
    "Pop bailable y energética (colaboración)": {
        "bailabilidad": 0.78, "energia": 0.87, "valencia": 0.4, "acustica": 0.45,
        "tempo": 137, "duracion_min": 3.5, "volumen_db": -5.3, "anio": 2020,
        "colaboracion": 1, "genero": "pop",
    },
    "Indie acústica y tranquila": {
        "bailabilidad": 0.3, "energia": 0.2, "valencia": 0.3, "acustica": 0.8,
        "tempo": 90, "duracion_min": 4.2, "volumen_db": -12, "anio": 2015,
        "colaboracion": 0, "genero": "indie",
    },
}


def _llamar(url: str, datos: dict | None = None):
    peticion = urllib.request.Request(
        url,
        data=json.dumps(datos).encode() if datos is not None else None,
        headers={"Content-Type": "application/json"},
    )
    # El plan gratuito de Render puede tardar ~1 min en "despertar"
    with urllib.request.urlopen(peticion, timeout=90) as r:
        return json.loads(r.read())


def main(base: str = "http://127.0.0.1:8000") -> int:
    base = base.rstrip("/")
    print(f"Probando {base}")
    try:
        print("GET /salud ->", _llamar(f"{base}/salud"))
        for nombre, cancion in EJEMPLOS.items():
            print(f"POST /predict [{nombre}] ->", _llamar(f"{base}/predict", cancion))
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"No se pudo conectar: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:2]))
