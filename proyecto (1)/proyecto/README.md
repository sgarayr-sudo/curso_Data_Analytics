# Predicción de popularidad de canciones

Servicio en línea que, a partir de las características de una canción, estima su
**popularidad (0-100)** con un modelo de regresión y la **probabilidad de que sea
un hit** (popularidad ≥ 70) con un modelo de clasificación.

Flujo del proyecto: `datos (2000 registros)` → `ML (regresión + clasificación)` →
`modelo.pkl` → `API en línea` (localhost / servidor open source / Render).

## Estructura
```
data/canciones.csv              datos
models/modelo.pkl               artefacto: regresión + clasificación + metadatos
src/
  variables.py                  rutas, columnas, umbral de hit
  artefacto.py                  guardar y cargar el .pkl
  entrenar_regresion.py         entrena y guarda el regresor
  entrenar_clasificacion.py     entrena y guarda el clasificador
  probar_servicio.py            prueba el servicio (local o Render)
  app/main.py, schemas.py       API FastAPI
  app/static/index.html         interfaz web "Hit Lab" (se sirve en /)
tests/                          pruebas con pytest
render.yaml                     configuración de despliegue en Render
requirements.txt
```

## Resultados (conjunto de prueba)
| Modelo | Elegido | Métricas |
|---|---|---|
| Regresión | Ridge | R² 0.65 · MAE 6.2 · RMSE 7.6 |
| Clasificación | Regresión logística | AUC 0.91 · accuracy 0.78 · F1 0.62 |

**Sin fuga de datos:** se excluyen `reproducciones_sem1` (solo se conoce después
del lanzamiento, correlación 0.99 con la popularidad) y `es_hit` (se calcula a
partir de la popularidad). Con ellas el modelo parecería casi perfecto, pero no
serviría para predecir antes de publicar.

## 1. Localhost
```bash
pip install -r requirements.txt
python -m src.entrenar_regresion          # opcional, el .pkl ya viene incluido
python -m src.entrenar_clasificacion      # opcional
uvicorn src.app.main:app --reload
```
Interfaz web (Hit Lab): http://127.0.0.1:8000/
Documentación interactiva: http://127.0.0.1:8000/docs

Probar con ejemplos: `python -m src.probar_servicio`
Tests: `python -m pytest`

Ejemplo de petición:
```bash
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d '{
  "bailabilidad":0.78,"energia":0.87,"valencia":0.4,"acustica":0.45,
  "tempo":137,"duracion_min":3.5,"volumen_db":-5.3,"anio":2020,
  "colaboracion":1,"genero":"pop"}'
```
Respuesta:
```json
{"popularidad_estimada": 82.4, "probabilidad_hit": 0.986, "es_hit_predicho": true}
```

Endpoints: `GET /` (interfaz web) · `GET /api` · `GET /salud` · `GET /modelo` (métricas) · `POST /predict`

## 2. Servidor open source (Docker)
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY models ./models
COPY data ./data
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
```bash
docker build -t canciones-api .
docker run -p 8000:8000 canciones-api
```

## 3. Plan gratuito en Render
1. Sube el proyecto a GitHub (incluye `models/modelo.pkl`).
2. En render.com: **New > Blueprint** y elige el repositorio; Render lee `render.yaml`.
   (Alternativa manual: New > Web Service con Build `pip install -r requirements.txt`
   y Start `uvicorn src.app.main:app --host 0.0.0.0 --port $PORT`.)
3. Cuando termine, prueba: `python -m src.probar_servicio https://TU-APP.onrender.com`

En el plan gratuito el servicio se duerme tras un rato sin tráfico; la primera
petición puede tardar cerca de un minuto.

> Si cambias la versión de scikit-learn, vuelve a entrenar los modelos para
> regenerar `models/modelo.pkl`.
