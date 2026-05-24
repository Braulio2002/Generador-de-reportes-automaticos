# -*- coding: utf-8 -*-
"""
Modelos de Datos del Dominio
----------------------------
Define las entidades y DTOs (Data Transfer Objects) tipados fuertemente
que viajan entre las diferentes capas de la aplicación modular.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import List, Dict


@dataclass(frozen=True)
class LimpiezaInfo:
    """Información detallada sobre la limpieza de datos realizada."""
    filas_originales: int
    filas_vacias_eliminadas: int
    filas_limpias: int
    columnas_normalizadas: int


@dataclass(frozen=True)
class EstadisticaNumerica:
    """Resumen estadístico de alta precisión (Decimal) de una columna numérica."""
    columna: str
    suma: Decimal
    promedio: Decimal
    minimo: Decimal
    maximo: Decimal


@dataclass(frozen=True)
class MetricasReporte:
    """Métricas generales sobre el estado físico, completitud y calidad del dataset."""
    total_registros: int
    total_columnas: int
    total_vacios: int
    total_duplicados: int
    columnas_numericas: List[str]
    columnas_categoricas: List[str]
    filas_vacias_eliminadas: int
    columnas_con_mas_nulos: Dict[str, int]
