"""Esquemas de entrada y salida de la API."""
from enum import Enum

from pydantic import BaseModel, Field

from src.variables import GENEROS

Genero = Enum("Genero", {g: g for g in GENEROS}, type=str)


class Cancion(BaseModel):
    bailabilidad: float = Field(..., ge=0, le=1, examples=[0.75])
    energia: float = Field(..., ge=0, le=1, examples=[0.8])
    valencia: float = Field(..., ge=0, le=1, examples=[0.6])
    acustica: float = Field(..., ge=0, le=1, examples=[0.2])
    tempo: float = Field(..., ge=40, le=250, examples=[120])
    duracion_min: float = Field(..., gt=0, le=20, examples=[3.5])
    volumen_db: float = Field(..., ge=-60, le=5, examples=[-6])
    anio: int = Field(..., ge=1950, le=2100, examples=[2024])
    colaboracion: int = Field(..., ge=0, le=1, examples=[1])
    genero: Genero = Field(..., examples=["pop"])


class Prediccion(BaseModel):
    popularidad_estimada: float = Field(..., description="Escala 0-100")
    probabilidad_hit: float | None = Field(
        None, description="Probabilidad de que la canción sea un hit (popularidad >= 70)"
    )
    es_hit_predicho: bool | None = None
