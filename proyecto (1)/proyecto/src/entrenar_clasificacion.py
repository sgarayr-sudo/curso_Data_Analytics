"""Entrena el modelo de CLASIFICACIÓN (predice si la canción será un hit).

es_hit = 1 cuando popularidad >= 70. Usa solo características previas al
lanzamiento, igual que la regresión.

Uso (desde la raíz del proyecto):
    python -m src.entrenar_clasificacion
"""
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline

from src import artefacto
from src.entrenar_regresion import crear_preprocesador
from src.variables import CARACTERISTICAS, OBJETIVO_CLASIFICACION, RUTA_DATOS, SEMILLA


def main() -> dict:
    df = pd.read_csv(RUTA_DATOS)
    X, y = df[CARACTERISTICAS], df[OBJETIVO_CLASIFICACION]
    # stratify: los hits son ~20% de los datos, se mantiene esa proporción
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, random_state=SEMILLA, stratify=y
    )

    candidatos = {
        "LogisticRegression": (
            LogisticRegression(max_iter=1000, class_weight="balanced"),
            {"modelo__C": [0.1, 1, 10]},
        ),
        "RandomForest": (
            RandomForestClassifier(n_estimators=300, class_weight="balanced",
                                   random_state=SEMILLA, n_jobs=-1),
            {"modelo__max_depth": [None, 10], "modelo__min_samples_leaf": [1, 3, 5]},
        ),
        "GradientBoosting": (
            GradientBoostingClassifier(random_state=SEMILLA),
            {"modelo__n_estimators": [100, 200],
             "modelo__learning_rate": [0.03, 0.1],
             "modelo__max_depth": [2, 3]},
        ),
    }

    comparacion, ajustados = {}, {}
    for nombre, (modelo, grid) in candidatos.items():
        pipe = Pipeline([("prep", crear_preprocesador()), ("modelo", modelo)])
        busqueda = GridSearchCV(pipe, grid, cv=5, scoring="roc_auc", n_jobs=-1)
        busqueda.fit(X_tr, y_tr)
        pred = busqueda.predict(X_te)
        proba = busqueda.predict_proba(X_te)[:, 1]
        comparacion[nombre] = {
            "AUC_cv": round(float(busqueda.best_score_), 4),
            "AUC_test": round(float(roc_auc_score(y_te, proba)), 4),
            "accuracy_test": round(float(accuracy_score(y_te, pred)), 4),
            "F1_test": round(float(f1_score(y_te, pred)), 4),
        }
        ajustados[nombre] = busqueda.best_estimator_
        print(f"{nombre:18s} {comparacion[nombre]}")

    mejor = max(comparacion, key=lambda k: comparacion[k]["AUC_cv"])
    metricas = {"modelo": mejor, **comparacion[mejor], "comparacion": comparacion}
    print(f"\nMejor modelo (AUC en validación cruzada): {mejor}")

    final = ajustados[mejor].fit(X, y)
    artefacto.guardar_parte(artefacto.CLASIFICACION, final, metricas)
    print("Clasificación guardada en models/modelo.pkl")
    return metricas


if __name__ == "__main__":
    main()
