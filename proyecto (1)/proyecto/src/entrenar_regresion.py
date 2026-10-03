"""Entrena el modelo de REGRESIÓN (predice popularidad 0-100).

Uso (desde la raíz del proyecto):
    python -m src.entrenar_regresion
"""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src import artefacto
from src.variables import (
    CARACTERISTICAS, CATEGORICAS, NUMERICAS, OBJETIVO_REGRESION,
    RUTA_DATOS, SEMILLA,
)


def crear_preprocesador() -> ColumnTransformer:
    return ColumnTransformer([
        ("num", StandardScaler(), NUMERICAS),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAS),
    ])


def main() -> dict:
    df = pd.read_csv(RUTA_DATOS)
    X, y = df[CARACTERISTICAS], df[OBJETIVO_REGRESION]
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, random_state=SEMILLA
    )

    candidatos = {
        "Ridge": (Ridge(), {"modelo__alpha": [0.1, 1, 10, 100]}),
        "RandomForest": (
            RandomForestRegressor(n_estimators=300, random_state=SEMILLA, n_jobs=-1),
            {"modelo__max_depth": [None, 10, 20], "modelo__min_samples_leaf": [1, 3, 5]},
        ),
        "GradientBoosting": (
            GradientBoostingRegressor(random_state=SEMILLA),
            {"modelo__n_estimators": [100, 200],
             "modelo__learning_rate": [0.03, 0.1],
             "modelo__max_depth": [2, 3]},
        ),
    }

    comparacion, ajustados = {}, {}
    for nombre, (modelo, grid) in candidatos.items():
        pipe = Pipeline([("prep", crear_preprocesador()), ("modelo", modelo)])
        busqueda = GridSearchCV(pipe, grid, cv=5, scoring="r2", n_jobs=-1)
        busqueda.fit(X_tr, y_tr)
        pred = busqueda.predict(X_te)
        comparacion[nombre] = {
            "R2_cv": round(float(busqueda.best_score_), 4),
            "R2_test": round(float(r2_score(y_te, pred)), 4),
            "MAE_test": round(float(mean_absolute_error(y_te, pred)), 3),
            "RMSE_test": round(float(np.sqrt(mean_squared_error(y_te, pred))), 3),
        }
        ajustados[nombre] = busqueda.best_estimator_
        print(f"{nombre:18s} {comparacion[nombre]}")

    mejor = max(comparacion, key=lambda k: comparacion[k]["R2_cv"])
    metricas = {"modelo": mejor, **comparacion[mejor], "comparacion": comparacion}
    print(f"\nMejor modelo (R2 en validación cruzada): {mejor}")

    # Se reajusta con todos los datos para el servicio final
    final = ajustados[mejor].fit(X, y)
    artefacto.guardar_parte(artefacto.REGRESION, final, metricas)
    print("Regresión guardada en models/modelo.pkl")
    return metricas


if __name__ == "__main__":
    main()
